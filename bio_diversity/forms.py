import inspect
import math
from datetime import date, datetime

import pytz
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.utils.timezone import make_aware
from django.utils.translation import gettext
import pandas as pd
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


from bio_diversity import models
from bio_diversity.utils import comment_parser, enter_tank_contx, enter_indvd, year_coll_splitter, enter_env, \
    create_movement_evnt, enter_grpd, enter_anix, val_unit_splitter, parse_concentration


class CreatePrams(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()


class CreateDatePrams(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['start_date'].widget = forms.DateInput(attrs={"placeholder": "Click to select a date..",
                                                                  "class": "fp-date"})
        self.fields['end_date'].widget = forms.DateInput(attrs={"placeholder": "Click to select a date..",
                                                                "class": "fp-date"})

    def clean(self):
        cleaned_data = super().clean()
        # we have to make sure
        # 1) the end date is after the start date and
        # 2) valid is false if today is after end_date
        end_date = cleaned_data.get("end_date")
        valid = cleaned_data.get("det_valid")
        if end_date:
            start_date = cleaned_data.get("start_date")
            today = date.today()
            if end_date and start_date and end_date < start_date:
                self.add_error('end_date', gettext(
                    "The end date must be after the start date!"
                ))
            elif end_date and valid and end_date < today:
                self.add_error('det_valid', gettext("Cannot be valid after end date"))

        return self.cleaned_data


class CreateTimePrams(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['start_datetime'].widget = forms.HiddenInput()
        self.fields['start_datetime'].required = False
        self.fields['end_datetime'].widget = forms.HiddenInput()
        self.fields['end_datetime'].required = False
        self.fields['start_date'] = forms.DateField(widget=forms.DateInput(attrs={"placeholder": "Click to select a date...", "class": "fp-date"}))
        self.fields['end_date'] = forms.DateField(required=False, widget=forms.DateInput(attrs={"placeholder": "Click to select a date...", "class": "fp-date"}))
        self.fields['start_time'] = forms.CharField(required=False, widget=forms.DateInput(attrs={"placeholder": "Click to select a time...", "class": "fp-time"}))
        self.fields['end_time'] = forms.CharField(required=False, widget=forms.DateInput(attrs={"placeholder": "Click to select a time...", "class": "fp-time"}))

    def clean(self):
        cleaned_data = super().clean()

        if not self.is_valid():
            return cleaned_data
        # we have to make sure
        # the end datetime is after the start datetime
        # and set the datetime values
        if cleaned_data["start_time"]:
            start_time = datetime.strptime(cleaned_data["start_time"],
                                           '%H:%M').time().replace(tzinfo=pytz.UTC)
        else:
            start_time = datetime.min.time().replace(tzinfo=pytz.UTC)
        cleaned_data["start_datetime"] = datetime.combine(cleaned_data["start_date"], start_time)
        if cleaned_data["end_date"]:
            if cleaned_data["end_time"]:
                end_time = datetime.strptime(cleaned_data["end_time"],
                                             '%H:%M').time().replace(tzinfo=pytz.UTC)
            else:
                end_time = datetime.min.time().replace(tzinfo=pytz.UTC)
            cleaned_data["end_datetime"] = datetime.combine(cleaned_data["end_date"], end_time)

        end_date = cleaned_data.get("end_date")
        end_time = cleaned_data.get("end_time")
        start_time = cleaned_data.get("start_time")
        if end_date:
            start_date = cleaned_data.get("start_date")
            if end_date and start_date and end_date < start_date:
                self.add_error('end_date', gettext(
                    "The end date must be after the start date!"
                ))
            elif end_date and start_date and end_date == start_date:
                if end_time and start_time and end_time < start_time:
                    self.add_error('end_time', gettext(
                        "The end date must be after the start date!"
                    ))
        return self.cleaned_data


class AnidcForm(CreatePrams):
    class Meta:
        model = models.AnimalDetCode
        exclude = []


class AnixForm(CreatePrams):

    class Meta:
        model = models.AniDetailXref
        exclude = []
        widgets = {
            'final_contx_flag': forms.NullBooleanSelect()
        }


class AdscForm(CreatePrams):
    class Meta:
        model = models.AniDetSubjCode
        exclude = []


class CntForm(CreatePrams):
    class Meta:
        model = models.Count
        exclude = []


class CntcForm(CreatePrams):
    class Meta:
        model = models.CountCode
        exclude = []


class CntdForm(CreatePrams):
    class Meta:
        model = models.CountDet
        exclude = []


class CollForm(CreatePrams):
    class Meta:
        model = models.Collection
        exclude = []


class CommentKeywordsForm(forms.ModelForm):

    model = None

    class Meta:
        fields = "__all__"
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["adsc_id"].queryset = models.AniDetSubjCode.objects.filter(anidc_id__name__iexact="Animal Health")


CommentKeywordsFormset = modelformset_factory(
    model=models.CommentKeywords,
    form=CommentKeywordsForm,
    extra=1,
)


class ContdcForm(CreatePrams):
    class Meta:
        model = models.ContainerDetCode
        exclude = []


class ContxForm(CreatePrams):
    class Meta:
        model = models.ContainerXRef
        exclude = []


class CdscForm(CreatePrams):
    class Meta:
        model = models.ContDetSubjCode
        exclude = []


class CupForm(CreatePrams):
    class Meta:
        model = models.Cup
        exclude = []


class CupdForm(CreateDatePrams):
    class Meta:
        model = models.CupDet
        exclude = []


class DataForm(CreatePrams):

    class Meta:
        model = models.DataLoader
        exclude = []

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(DataForm, self).__init__(*args, **kwargs)

    def save(self):
        # never save this form to db
        super().save(commit=False)

    def clean(self):
        cleaned_data = super().clean()

        if not self.is_valid():
            return cleaned_data

        log_data = "Loading Data Results: \n"
        rows_parsed = 0
        rows_entered = 0

        # --------------------------ELECTROFISHING DATA ENTRY-----------------------------------
        if cleaned_data["evntc_id"].__str__() == "Electrofishing" and cleaned_data["facic_id"].__str__() == "Coldbrook":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl',
                                     converters={'Year': str, 'Month': str, 'Day': str})
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True

            self.request.session["load_success"] = True
            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    row_datetime = datetime.strptime(row["Year"] + row["Month"] + row["Day"],
                                                     "%Y%b%d").replace(tzinfo=pytz.UTC)
                    loc = models.Location(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          locc_id=models.LocCode.objects.filter(name__icontains="Electrofishing site").get(),
                                          rive_id=models.RiverCode.objects.filter(name=row["River"]).get(),
                                          relc_id=models.ReleaseSiteCode.objects.filter(name__iexact=row["Site"]).get(),
                                          loc_date=row_datetime,
                                          comments=row["Comments"],
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
                    try:
                        loc.clean()
                        loc.save()
                        row_entered = True
                    except ValidationError:
                        loc = models.Location.objects.filter(evnt_id=loc.evnt_id, locc_id=loc.locc_id,
                                                             rive_id=loc.rive_id, subr_id=loc.subr_id,
                                                             relc_id=loc.relc_id, loc_date=loc.loc_date).get()

                    if enter_env(row["temp"], row_datetime, cleaned_data, "Temperature", loc_id=loc,):
                        row_entered = True

                    cnt = False
                    if not math.isnan(row["# of salmon collected"]):
                        cnt = models.Count(loc_id_id=loc.pk,
                                           spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                           cntc_id=models.CountCode.objects.filter(name__iexact="Fish Caught").get(),
                                           cnt=row["# of salmon collected"],
                                           est=False,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            cnt.clean()
                            cnt.save()
                            row_entered = True
                        except ValidationError:
                            cnt = models.Count.objects.filter(loc_id=cnt.loc_id, cntc_id=cnt.cntc_id, cnt=cnt.cnt).get()

                    elif not math.isnan(row["# of salmon observed"]):
                        cnt = models.Count(loc_id_id=loc.pk,
                                           spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                           cntc_id=models.CountCode.objects.filter(
                                               name__iexact="Fish Observed").get(),
                                           cnt=row["# of salmon observed"],
                                           est=False,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            cnt.clean()
                            cnt.save()
                            row_entered = True
                        except ValidationError:
                            cnt = models.Count.objects.filter(loc_id=cnt.loc_id, cntc_id=cnt.cntc_id, cnt=cnt.cnt).get()
                    if cnt:
                        if not math.isnan(row["fishing seconds"]):
                            cntd = models.CountDet(cnt_id=cnt,
                                                   anidc_id=models.AnimalDetCode.objects.filter(name__iexact="Electrofishing Seconds").get(),
                                                   det_val=row["fishing seconds"],
                                                   qual_id=models.QualCode.objects.filter(name="Good").get(),
                                                   created_by=cleaned_data["created_by"],
                                                   created_date=cleaned_data["created_date"],
                                                   )
                            try:
                                cntd.clean()
                                cntd.save()
                                row_entered = True
                            except ValidationError:
                                pass

                        if not math.isnan(row["Voltage"]):
                            cntd = models.CountDet(cnt_id=cnt,
                                                   anidc_id=models.AnimalDetCode.objects.filter(name__iexact="Voltage").get(),
                                                   det_val=row["Voltage"],
                                                   qual_id=models.QualCode.objects.filter(name="Good").get(),
                                                   created_by=cleaned_data["created_by"],
                                                   created_date=cleaned_data["created_date"],
                                                   )
                            try:
                                cntd.clean()
                                cntd.save()
                                row_entered = True
                            except ValidationError:
                                pass

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1
            if parsed:
                try:
                    anix_grp_qs = models.AniDetailXref.objects.filter(evnt_id=cleaned_data["evnt_id"],
                                                                      grp_id__isnull=False,
                                                                      indv_id__isnull=True,
                                                                      contx_id__isnull=True,
                                                                      indvt_id__isnull=True,
                                                                      loc_id__isnull=True,
                                                                      pair_id__isnull=True)
                    if anix_grp_qs.count() == 0:

                        grp = models.Group(spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                           stok_id=models.StockCode.objects.filter(name=data["River"][0]).get(),
                                           coll_id=models.Collection.objects.filter(name__icontains=data["purpose"][0][:8]).get(),
                                           grp_year=data["Year"][0],
                                           grp_valid=True,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            grp.clean()
                            grp.save()
                        except ValidationError:
                            grp = models.Group.objects.filter(spec_id=grp.spec_id,
                                                              stok_id=grp.stok_id,
                                                              coll_id=grp.coll_id).get()

                        anix_grp = enter_anix(cleaned_data, grp_pk=grp.pk)
                    elif anix_grp_qs.count() == 1:
                        anix_grp = anix_grp_qs.get()
                        grp = anix_grp.grp_id

                    first_row_date = datetime.strptime(data["Year"][0] + data["Month"][0] + data["Day"][0],
                                                       "%Y%b%d").replace(tzinfo=pytz.UTC)
                    enter_grpd(anix_grp.pk, cleaned_data, first_row_date, data["# of salmon collected"].sum(), "Number of Fish")

                    enter_tank_contx(cleaned_data["tank_id"].name, cleaned_data, True, None, grp.pk, False)

                except Exception as err:
                    log_data += "Error parsing common data: \n"
                    log_data += "\n Error: {}".format(err.__str__())
                    self.request.session["load_success"] = False
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to" \
                        " database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # --------------------------ELECTROFISHING MACTAQUAC DATA ENTRY-----------------------------------
        elif cleaned_data["evntc_id"].__str__() == "Electrofishing" and \
                cleaned_data["facic_id"].__str__() == "Mactaquac":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], header=1, engine='openpyxl')
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True

            self.request.session["load_success"] = True
            for row in data_dict:
                row_parsed = True
                row_entered = False
                row_date = datetime.strptime(str(row["Year"])+str(row["Month"])+str(row["Day"]), "%Y%b%d").replace(tzinfo=pytz.UTC)
                try:
                    loc = models.Location(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          locc_id=models.LocCode.objects.first(),
                                          relc_id=models.ReleaseSiteCode.objects.filter(
                                              name__iexact=row["Location Name"]).get(),
                                          loc_date=row_date,
                                          comments=row["Comments"],
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
                    try:
                        loc.clean()
                        loc.save()
                        row_entered = True
                    except ValidationError:
                        loc = models.Location.objects.filter(evnt_id=loc.evnt_id, locc_id=loc.locc_id,
                                                             rive_id=loc.rive_id, subr_id=loc.subr_id,
                                                             relc_id=loc.relc_id, loc_date=loc.loc_date).get()

                    if enter_env(row["Temperature"], row_date, cleaned_data, "Temperature", loc_id=loc,):
                        row_entered = True

                    cnt = False
                    if not math.isnan(row["# Parr Collected"]):
                        cnt = models.Count(loc_id_id=loc.pk,
                                           spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                           cntc_id=models.CountCode.objects.filter(
                                               name__iexact="Fish Caught").get(),
                                           cnt=row["# Parr Collected"],
                                           est=False,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            cnt.clean()
                            cnt.save()
                            row_entered = True
                        except ValidationError:
                            cnt = models.Count.objects.filter(loc_id=cnt.loc_id, cntc_id=cnt.cntc_id,
                                                              cnt=cnt.cnt).get()

                    elif not math.isnan(row["# Parr Observed"]):
                        cnt = models.Count(loc_id_id=loc.pk,
                                           spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                           cntc_id=models.CountCode.objects.filter(
                                               name__iexact="Fish Observed").get(),
                                           cnt=row["# Parr Observed"],
                                           est=False,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            cnt.clean()
                            cnt.save()
                            row_entered = True
                        except ValidationError:
                            cnt = models.Count.objects.filter(loc_id=cnt.loc_id, cntc_id=cnt.cntc_id,
                                                              cnt=cnt.cnt).get()
                    if cnt:
                        if not math.isnan(row["Fishing seconds"]):
                            cntd = models.CountDet(cnt_id=cnt,
                                                   anidc_id=models.AnimalDetCode.objects.filter(
                                                       name__iexact="Electrofishing Seconds").get(),
                                                   det_val=row["Fishing seconds"],
                                                   qual_id=models.QualCode.objects.filter(name="Good").get(),
                                                   created_by=cleaned_data["created_by"],
                                                   created_date=cleaned_data["created_date"],
                                                   )
                            try:
                                cntd.clean()
                                cntd.save()
                                row_entered = True
                            except ValidationError:
                                pass

                        if not math.isnan(row["Voltage"]):
                            cntd = models.CountDet(cnt_id=cnt,
                                                   anidc_id=models.AnimalDetCode.objects.filter(
                                                       name__iexact="Voltage").get(),
                                                   det_val=row["Voltage"],
                                                   qual_id=models.QualCode.objects.filter(name="Good").get(),
                                                   created_by=cleaned_data["created_by"],
                                                   created_date=cleaned_data["created_date"],
                                                   )
                            try:
                                cntd.clean()
                                cntd.save()
                                row_entered = True
                            except ValidationError:
                                pass

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1
            if parsed:
                try:
                    relc = models.ReleaseSiteCode.objects.filter(name__iexact=data["Location Name"][0]).get()

                    anix_grp_qs = models.AniDetailXref.objects.filter(evnt_id=cleaned_data["evnt_id"],
                                                                      grp_id__isnull=False,
                                                                      indv_id__isnull=True,
                                                                      contx_id__isnull=True,
                                                                      indvt_id__isnull=True,
                                                                      loc_id__isnull=True,
                                                                      pair_id__isnull=True)

                    if anix_grp_qs.count() == 0:
                        grp = models.Group(spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                           stok_id=models.StockCode.objects.filter(name__icontains=relc.rive_id.name).get(),
                                           coll_id=models.Collection.objects.filter(name__icontains="Fall Parr").get(),
                                           grp_year=data["Year"][0],
                                           grp_valid=True,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            grp.clean()
                            grp.save()
                        except ValidationError:
                            grp = models.Group.objects.filter(spec_id=grp.spec_id, stok_id=grp.stok_id,
                                                              grp_year=grp.grp_year, coll_id=grp.coll_id).get()
                        anix_grp = enter_anix(cleaned_data, grp_pk=grp.pk)
                    elif anix_grp_qs.count() == 1:
                        anix_grp = anix_grp_qs.get()
                        grp = anix_grp.grp_id

                    first_row_date = datetime.strptime(str(data["Year"][0])+str(data["Month"][0])+str(data["Day"][0]), "%Y%b%d").replace(tzinfo=pytz.UTC)
                    enter_grpd(anix_grp.pk, cleaned_data, first_row_date, data["# Parr Collected"].sum(), "Number of Fish")

                    enter_tank_contx(cleaned_data["tank_id"].name, cleaned_data, True, None, grp.pk, False)

                except Exception as err:
                    log_data += "Error parsing common data: \n"
                    log_data += "\n Error: {}".format(err.__str__())
                    self.request.session["load_success"] = False
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to" \
                        " database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # ---------------------------TAGGING DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "PIT Tagging" and cleaned_data["facic_id"].__str__() == "Coldbrook":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl', header=0,
                                     converters={'to tank': str, 'Year': str, 'Month': str, 'Day': str})
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True
            grp_id = False
            try:
                year, coll = year_coll_splitter(data["Group"][0])
                grp_qs = models.Group.objects.filter(stok_id__name=data_dict[0]["Stock"],
                                                     coll_id__name__icontains=coll,
                                                     grp_year=year)
                if len(grp_qs) == 1:
                    grp_id = grp_qs.get().pk
                elif len(grp_qs) > 1:
                    for grp in grp_qs:
                        tank_list = grp.current_tank()
                        if data["from Tank"][0] in [tank.name for tank in tank_list]:
                            grp_id = grp.pk

            except Exception as err:
                log_data += "Error finding origin group (check first row): \n"
                log_data += "Error: {}\n\n".format(err.__str__())
                self.request.session["load_success"] = False

            if grp_id:
                enter_anix(cleaned_data, grp_pk=grp_id)

            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    year, coll = year_coll_splitter(row["Group"])
                    row_datetime = datetime.strptime(row["Year"] + row["Month"] + row["Day"],
                                                     "%Y%b%d").replace(tzinfo=pytz.UTC)
                    row_date =row_datetime.date()
                    if type(row["Universal Fish ID"]) == float:
                        indv_ufid = None
                    else:
                        indv_ufid = row["Universal Fish ID"]
                    indv = models.Individual(grp_id_id=grp_id,
                                             spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                                             stok_id=models.StockCode.objects.filter(name=row["Stock"]).get(),
                                             coll_id=models.Collection.objects.filter(name__icontains=coll).get(),
                                             indv_year=year,
                                             pit_tag=row["PIT tag"],
                                             ufid=indv_ufid,
                                             indv_valid=True,
                                             comments=row["comments"],
                                             created_by=cleaned_data["created_by"],
                                             created_date=cleaned_data["created_date"],
                                             )
                    try:
                        indv.clean()
                        indv.save()
                        row_entered = True
                    except (ValidationError, IntegrityError):
                        indv = models.Individual.objects.filter(pit_tag=indv.pit_tag).get()

                    if create_movement_evnt(row["from Tank"], row["to tank"], cleaned_data, row_datetime, indv_pk=indv.pk):
                        row_entered = True

                    anix_indv = enter_anix(cleaned_data, indv_pk=indv.pk)

                    anix_grp = enter_anix(cleaned_data, indv_pk=indv.pk, grp_pk=grp_id)

                    if enter_indvd(anix_indv.pk, cleaned_data, row_date, row["Length (cm)"], "Length", None):
                        row_entered = True

                    if enter_indvd(anix_indv.pk, cleaned_data, row_date, row["Weight (g)"], "Weight", None):
                        row_entered = True

                    if enter_indvd(anix_indv.pk, cleaned_data, row_date, row["Vial"], "Vial", None):
                        row_entered = True

                    if enter_indvd(anix_indv.pk, cleaned_data, row_date, row["Box"], "Box", None):
                        row_entered = True

                    if enter_indvd(anix_indv.pk, cleaned_data, row_date, row["location"], "Box Location", None):
                        row_entered = True

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1
            if not parsed:
                self.request.session["load_success"] = False
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

            # ---------------------------TAGGING MACTAQUAC DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "PIT Tagging" and cleaned_data["facic_id"].__str__() == "Mactaquac":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl', header=0,
                                     converters={'to tank': str, "PIT": str, 'Year': str, 'Month': str, 'Day': str})
                data["Comments"] = data["Comments"].fillna('')
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True
            grp_id = False
            try:

                year, coll = year_coll_splitter(data["Collection"][0])
                grp_qs = models.Group.objects.filter(stok_id__name=data_dict[0]["Stock"],
                                                     coll_id__name__icontains=coll,
                                                     grp_year=year)
                if len(grp_qs) == 1:
                    grp_id = grp_qs.get().pk
                elif len(grp_qs) > 1:
                    for grp in grp_qs:
                        tank_list = grp.current_tank()
                        if data["Origin Pond"][0] in [tank.name for tank in tank_list]:
                            grp_id = grp.pk

            except Exception as err:
                log_data += "Error finding origin group (check first row): \n"
                log_data += "Error: {}\n\n".format(err.__str__())
                self.request.session["load_success"] = False

            if grp_id:
                anix_grp = enter_anix(cleaned_data, grp_pk=grp_id)

            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    year, coll = year_coll_splitter(row["Collection"])
                    row_datetime = datetime.strptime(row["Year"] + row["Month"] + row["Day"],
                                                 "%Y%b%d").replace(tzinfo=pytz.UTC)
                    indv = models.Individual(grp_id_id=grp_id,
                                             spec_id=models.SpeciesCode.objects.filter(name__icontains="Salmon").get(),
                                             stok_id=models.StockCode.objects.filter(name=row["Stock"]).get(),
                                             coll_id=models.Collection.objects.filter(name__icontains=coll).get(),
                                             indv_year=year,
                                             pit_tag=row["PIT"],
                                             indv_valid=True,
                                             comments=row["Comments"],
                                             created_by=cleaned_data["created_by"],
                                             created_date=cleaned_data["created_date"],
                                             )
                    try:
                        indv.clean()
                        indv.save()
                        row_entered = True
                    except (ValidationError, IntegrityError):
                        indv = models.Individual.objects.filter(pit_tag=indv.pit_tag).get()

                    if create_movement_evnt(row["Origin Pond"], row["Destination Pond"], cleaned_data, row_datetime, indv_pk=indv.pk):
                        row_entered = True

                    anix_indv = enter_anix(cleaned_data, indv_pk=indv.pk)

                    anix_grp = enter_anix(cleaned_data, indv_pk=indv.pk, grp_pk=grp_id)

                    if enter_indvd(anix_indv.pk, cleaned_data, row_datetime.date(), row["Length (cm)"], "Length", None):
                        row_entered = True

                    if enter_indvd(anix_indv.pk, cleaned_data, row_datetime.date(), row["Weight (g)"], "Weight", None):
                        row_entered = True

                    if enter_indvd(anix_indv.pk, cleaned_data, row_datetime.date(), row["Vial Number"], "Vial", None):
                        row_entered = True

                    if row["Precocity (Y/N)"].upper() == "Y":
                        if enter_indvd(anix_indv.pk, cleaned_data, row_datetime.date(), None, "Animal Health", "Precocity"):
                            row_entered = True

                    if row["Comments"]:
                        comment_parser(row["Comments"], anix_indv, det_date=row_datetime.date())
                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1
            if not parsed:
                self.request.session["load_success"] = False
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # ---------------------------MATURITY SORTING DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "Maturity Sorting" and cleaned_data["facic_id"].__str__() == "Mactaquac":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl', header=0,
                                     converters={'PIT': str, 'Year': str, 'Month': str, 'Day': str})
                data["COMMENTS"] = data["COMMENTS"].fillna('')
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True
            sex_dict = {"M": "Male",
                        "F": "Female",
                        "I": "Immature"}
            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    indv_qs = models.Individual.objects.filter(pit_tag=row["PIT"])
                    if len(indv_qs) == 1:
                        indv = indv_qs.get()
                    else:
                        row_entered = False
                        row_parsed = False
                        indv = False
                        log_data += "Error parsing row: \n"
                        log_data += str(row)
                        log_data += "\nFish with PIT {} not found in db\n".format(row["PIT"])

                    if indv:
                        anix_indv = enter_anix(cleaned_data, indv_pk=indv.pk)

                        row_datetime = datetime.strptime(row["Year"] + row["Month"] + row["Day"],
                                                         "%Y%b%d").replace(tzinfo=pytz.UTC)
                        row_date =row_datetime.date()
                        if enter_indvd(anix_indv.pk, cleaned_data, row_date, None, "Gender", sex_dict[row["SEX"]], comments=row["COMMENTS"]):
                            row_entered = True

                        if create_movement_evnt(row["ORIGIN POND"], row["DESTINATION POND"], cleaned_data, row_datetime,
                                                indv_pk=indv.pk):
                            row_entered = True

                        if row["COMMENTS"]:
                            comment_parser(row["COMMENTS"], anix_indv)
                    else:
                        break

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1
            if not parsed:
                self.request.session["load_success"] = False
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # ---------------------------MACTAQUAC WATER QUALITY DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "Water Quality Record" and cleaned_data["facic_id"].__str__() == "Mactaquac":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], engine='openpyxl', header=0,
                                     converters={'Pond': str, 'Year': str, 'Month': str, 'Day': str})
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True
            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    contx = enter_tank_contx(row["Pond"], cleaned_data, None, return_contx=True)
                    row_date = datetime.strptime(row["Year"] + row["Month"] + row["Day"],
                                                     "%Y%b%d").replace(tzinfo=pytz.UTC).date()
                    if not math.isnan(row["Time (24HR)"]):
                        row_time = row["Time (24HR)"].replace(tzinfo=pytz.UTC)
                    else:
                        row_time = None

                    if enter_env(row["Temp °C"], row_date, cleaned_data, "Temperature", contx=contx, env_start=row_time):
                        row_entered = True
                    if enter_env(row["DO%"], row_date, cleaned_data, "Oxygen Level", contx=contx, env_start=row_time):
                        row_entered = True
                    if enter_env(row["pH"], row_date, cleaned_data, "pH", contx=contx, env_start=row_time):
                        row_entered = True
                    if enter_env(row["Dissolved Nitrogen %"], row_date, cleaned_data, "Dissolved Nitrogen", contx=contx, env_start=row_time):
                        row_entered = True

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1
            if not parsed:
                self.request.session["load_success"] = False
            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # ---------------------------MACTAQUAC SPAWNING DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "Spawning" and cleaned_data["facic_id"].__str__() == "Mactaquac":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], header=5, sheet_name="RECORDED matings")
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True

            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    indv_qs = models.Individual.objects.filter(pit_tag=row["Pit or carlin"])
                    indv_qs_male = models.Individual.objects.filter(pit_tag=row["Pit or carlin.1"])
                    if len(indv_qs) == 1 and len(indv_qs_male) == 1:
                        indv_female = indv_qs.get()
                        indv_male = indv_qs_male.get()
                    else:
                        log_data += "Error parsing row: \n"
                        log_data += str(row)
                        log_data += "\nFish with PIT {} or PIT {} not found in db\n".format(row["Pit or carlin"], row["Pit or carlin.1"])
                        break

                    row_date = row["date"].date()
                    anix_female = enter_anix(cleaned_data, indv_pk=indv_female.pk)
                    anix_male = enter_anix(cleaned_data, indv_pk=indv_male.pk)

                    if enter_indvd(anix_female.pk, cleaned_data, row_date, None, "Gender", "Female"):
                        row_entered = True

                    if enter_indvd(anix_female.pk, cleaned_data, row_date, row["Ln"], "Length", None):
                        row_entered = True

                    if enter_indvd(anix_female.pk, cleaned_data, row_date, row["Wt"], "Weight", None):
                        row_entered = True

                    if enter_indvd(anix_male.pk, cleaned_data, row_date, None, "Gender", "Male"):
                        row_entered = True

                    if enter_indvd(anix_male.pk, cleaned_data, row_date, row["Ln.1"], "Length", None):
                        row_entered = True

                    if enter_indvd(anix_male.pk, cleaned_data, row_date, row["Wt.1"], "Weight", None):
                        row_entered = True

                    # pair
                    prio_dict = {"H": "High", "M": "Normal", "P": "Low"}
                    pair = models.Pairing(start_date=row_date,
                                          prio_id=models.PriorityCode.objects.filter(
                                              name__iexact=prio_dict[row["Pri..1"]]).get(),
                                          valid=True,
                                          indv_id=indv_female,
                                          comments=row["Comment"],
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
                    try:
                        pair.clean()
                        pair.save()
                        row_entered = True
                    except (ValidationError, IntegrityError):
                        pair = models.Pairing.objects.filter(start_date=row_date, indv_id=indv_female).get()

                    # sire
                    sire = models.Sire(prio_id=models.PriorityCode.objects.filter(name__iexact=prio_dict[row["Pri..1"]]).get(),
                                       pair_id=pair,
                                       indv_id=indv_male,
                                       choice=row["Choice"],
                                       comments=row["Comment.1"],
                                       created_by=cleaned_data["created_by"],
                                       created_date=cleaned_data["created_date"],
                                       )
                    try:
                        sire.clean()
                        sire.save()
                        row_entered = True
                    except (ValidationError, IntegrityError):
                        pass

                    anix_pair = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                                     pair_id=pair,
                                                     created_by=cleaned_data["created_by"],
                                                     created_date=cleaned_data["created_date"],
                                                     )
                    try:
                        anix_pair.clean()
                        anix_pair.save()
                        row_entered = True
                    except ValidationError:
                        pass

                    fecu_est = models.SpawnDet(pair_id=pair,
                                               spwndc_id=models.SpawnDetCode.objects.filter(name="Fecundity").get(),
                                               det_val=int(row["Exp. #"]),
                                               qual_id=models.QualCode.objects.filter(name="Calculated").get(),
                                               created_by=cleaned_data["created_by"],
                                               created_date=cleaned_data["created_date"],
                                               )
                    try:
                        fecu_est.clean()
                        fecu_est.save()
                        row_entered = True
                    except ValidationError:
                        pass

                    # grp
                    anix_grp_qs = models.AniDetailXref.objects.filter(evnt_id=cleaned_data["evnt_id"],
                                                                      grp_id__isnull=False,
                                                                      pair_id=pair,
                                                                      indv_id__isnull=True,
                                                                      contx_id__isnull=True,
                                                                      indvt_id__isnull=True,
                                                                      loc_id__isnull=True,
                                                                      )
                    if anix_grp_qs.count() == 0:

                        grp = models.Group(spec_id=indv_female.spec_id,
                                           stok_id=indv_female.stok_id,
                                           coll_id=models.Collection.objects.filter(name="F1").get(),
                                           grp_year=row_date.year,
                                           grp_valid=False,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            grp.clean()
                            grp.save()
                            anix_grp = enter_anix(cleaned_data, grp_pk=grp.pk)
                            anix_grp = enter_anix(cleaned_data, grp_pk=grp.pk, pair_pk=pair.pk)
                            grp.grp_valid = True
                            grp.save()
                        except ValidationError:
                            # recovering the group is only doable through the anix with both grp and pair.
                            # no way to find it here, so only make the group valid after anix's created.
                            pass

                    elif anix_grp_qs.count() == 1:
                        anix_grp = anix_grp_qs.get()
                        grp = anix_grp.grp_id

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1

            # matp
            indv_qs = models.Individual.objects.filter(pit_tag=data["Pit or carlin"][0])
            if len(indv_qs) == 1:
                indv_female = indv_qs.get()
                matp = models.MatingPlan(evnt_id_id=cleaned_data["evnt_id"].pk,
                                         stok_id=indv_female.stok_id,
                                         matp_xls=cleaned_data["data_csv"],
                                         created_by=cleaned_data["created_by"],
                                         created_date=cleaned_data["created_date"],
                                         )
                try:
                    matp.clean()
                    matp.save()
                except (ValidationError, IntegrityError):
                    pass

            if not parsed:
                self.request.session["load_success"] = False

            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # ---------------------------COLDBROOK SPAWNING DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "Spawning" and cleaned_data["facic_id"].__str__() == "Coldbrook":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], header=5, sheet_name="Recording")
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True

            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    indv_qs = models.Individual.objects.filter(pit_tag=row["Pit tag"])
                    indv_qs_male = models.Individual.objects.filter(pit_tag=row["Pit tag.1"])
                    if len(indv_qs) == 1 and len(indv_qs_male) == 1:
                        indv_female = indv_qs.get()
                        indv_male = indv_qs_male.get()
                    else:
                        log_data += "Error parsing row: \n"
                        log_data += str(row)
                        log_data += "\nFish with PIT {} or PIT {} not found in db\n".format(row["Pit tag"], row["Pit tag.1"])
                        break

                    row_date = datetime.strptime(row["date"], "%Y-%b-%d")
                    anix_female = enter_anix(cleaned_data, indv_pk=indv_female.pk)
                    anix_male = enter_anix(cleaned_data, indv_pk=indv_male.pk)

                    if enter_indvd(anix_female.pk, cleaned_data, row_date, row["Ln"], "Length", None):
                        row_entered = True

                    if enter_indvd(anix_female.pk, cleaned_data, row_date, row["Wt"], "Weight", None):
                        row_entered = True

                    if enter_indvd(anix_male.pk, cleaned_data, row_date, row["Ln.1"], "Length", None):
                        row_entered = True

                    if enter_indvd(anix_male.pk, cleaned_data, row_date, row["Wt.1"], "Weight", None):
                        row_entered = True

                    # pair
                    prio_dict = {"H": "High", "M": "Normal", "P": "Low"}
                    pair = models.Pairing(start_date=row_date,
                                          prio_id=models.PriorityCode.objects.filter(
                                              name__iexact=prio_dict[row["Pri..1"]]).get(),
                                          valid=True,
                                          indv_id=indv_female,
                                          comments=row["Comment"],
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
                    try:
                        pair.clean()
                        pair.save()
                        row_entered = True
                    except (ValidationError, IntegrityError):
                        pair = models.Pairing.objects.filter(start_date=row_date, indv_id=indv_female).get()

                    # sire
                    sire = models.Sire(prio_id=models.PriorityCode.objects.filter(name__iexact=prio_dict[row["Pri..1"]]).get(),
                                       pair_id=pair,
                                       indv_id=indv_male,
                                       choice=row["Choice"],
                                       comments=row["Comment.1"],
                                       created_by=cleaned_data["created_by"],
                                       created_date=cleaned_data["created_date"],
                                       )
                    try:
                        sire.clean()
                        sire.save()
                        row_entered = True
                    except (ValidationError, IntegrityError):
                        pass

                    anix_pair = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                                     pair_id=pair,
                                                     created_by=cleaned_data["created_by"],
                                                     created_date=cleaned_data["created_date"],
                                                     )
                    try:
                        anix_pair.clean()
                        anix_pair.save()
                        row_entered = True
                    except ValidationError:
                        pass

                    fecu_est = models.SpawnDet(pair_id=pair,
                                               spwndc_id=models.SpawnDetCode.objects.filter(name="Fecundity").get(),
                                               det_val=int(row["Exp. #"]),
                                               qual_id=models.QualCode.objects.filter(name="Calculated").get(),
                                               created_by=cleaned_data["created_by"],
                                               created_date=cleaned_data["created_date"],
                                               )
                    try:
                        fecu_est.clean()
                        fecu_est.save()
                        row_entered = True
                    except ValidationError:
                        pass

                    # grp
                    anix_grp_qs = models.AniDetailXref.objects.filter(evnt_id=cleaned_data["evnt_id"],
                                                                      grp_id__isnull=False,
                                                                      pair_id=pair,
                                                                      indv_id__isnull=True,
                                                                      contx_id__isnull=True,
                                                                      indvt_id__isnull=True,
                                                                      loc_id__isnull=True,
                                                                      )
                    if anix_grp_qs.count() == 0:

                        grp = models.Group(spec_id=indv_female.spec_id,
                                           stok_id=indv_female.stok_id,
                                           coll_id=models.Collection.objects.filter(name="F1").get(),
                                           grp_year=row_date.year,
                                           grp_valid=False,
                                           created_by=cleaned_data["created_by"],
                                           created_date=cleaned_data["created_date"],
                                           )
                        try:
                            grp.clean()
                            grp.save()
                            anix_grp = enter_anix(cleaned_data, grp_pk=grp.pk)
                            anix_grp = enter_anix(cleaned_data, grp_pk=grp.pk, pair_pk=pair.pk)
                            grp.grp_valid = True
                            grp.save()
                        except ValidationError:
                            # recovering the group is only doable through the anix with both grp and pair.
                            # no way to find it here, so only make the group valid after anix's created.
                            pass

                    elif anix_grp_qs.count() == 1:
                        anix_grp = anix_grp_qs.get()
                        grp = anix_grp.grp_id

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1

            # matp
            indv_qs = models.Individual.objects.filter(pit_tag=data["Pit tag"][0])
            if len(indv_qs) == 1:
                indv_female = indv_qs.get()
                matp = models.MatingPlan(evnt_id_id=cleaned_data["evnt_id"].pk,
                                         stok_id=indv_female.stok_id,
                                         matp_xls=cleaned_data["data_csv"],
                                         created_by=cleaned_data["created_by"],
                                         created_date=cleaned_data["created_date"],
                                         )
                try:
                    matp.clean()
                    matp.save()
                except (ValidationError, IntegrityError):
                    pass

            if not parsed:
                self.request.session["load_success"] = False

            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        # ---------------------------MACTAQUAC TREATMENT DATA ENTRY----------------------------------------
        elif cleaned_data["evntc_id"].__str__() == "Treatment" and cleaned_data["facic_id"].__str__() == "Mactaquac":
            try:
                data = pd.read_excel(cleaned_data["data_csv"], header=0, engine='openpyxl', sheet_name="Ponds")
                data_dict = data.to_dict('records')
            except Exception as err:
                log_data += "\n File format not valid: {}".format(err.__str__())
                self.request.session["log_data"] = log_data
                return
            parsed = True
            self.request.session["load_success"] = True

            for row in data_dict:
                row_parsed = True
                row_entered = False
                try:
                    row_date = row["Date"].date()

                    contx = enter_tank_contx(row["Pond / Trough"], cleaned_data, None, return_contx=True)
                    val, unit_str = val_unit_splitter(row["Amount"])
                    duration, time_unit = val_unit_splitter(row["Duration"])
                    row_concentration = parse_concentration(row["Concentration"])
                    envt = models.EnvTreatment(contx_id=contx,
                                               envtc_id=models.EnvTreatCode.objects.filter(name__icontains=row["Treatment Type"]).get(),
                                               lot_num=None,
                                               amt=val,
                                               unit_id=models.UnitCode.objects.filter(name__icontains=unit_str).get(),
                                               duration=60*duration,
                                               concentration=row_concentration.quantize(Decimal("0.000001")),
                                               created_by=cleaned_data["created_by"],
                                               created_date=cleaned_data["created_date"],
                                               )

                    try:
                        envt.clean()
                        envt.save()
                    except (ValidationError, IntegrityError):
                        pass

                    water_level, height_unit = val_unit_splitter(row["Pond Level During Treatment"])
                    enter_env(water_level, row_date, cleaned_data, "Water Level", contx=contx)

                except Exception as err:
                    parsed = False
                    self.request.session["load_success"] = False
                    log_data += "Error parsing row: \n"
                    log_data += str(row)
                    log_data += "\n Error: {}".format(err.__str__())
                    break
                if row_entered:
                    rows_entered += 1
                    rows_parsed += 1
                elif row_parsed:
                    rows_parsed += 1

            if not parsed:
                self.request.session["load_success"] = False

            log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered to " \
                        "database".format(rows_parsed, len(data_dict), rows_entered, len(data_dict))

        else:
            log_data = "Data loading not set up for this event type.  No data loaded."
        self.request.session["log_data"] = log_data


class DrawForm(CreatePrams):
    class Meta:
        model = models.Drawer
        exclude = []


class EnvForm(CreateTimePrams):
    class Meta:
        model = models.EnvCondition
        exclude = []
        widgets = {
        }


class EnvcForm(CreatePrams):
    class Meta:
        model = models.EnvCode
        exclude = []


class EnvcfForm(CreatePrams):
    class Meta:
        model = models.EnvCondFile
        exclude = []


class EnvscForm(CreatePrams):
    class Meta:
        model = models.EnvSubjCode
        exclude = []


class EnvtForm(CreatePrams):
    class Meta:
        model = models.EnvTreatment
        exclude = []


class EnvtcForm(CreatePrams):
    class Meta:
        model = models.EnvTreatCode
        exclude = []


class EvntForm(CreateTimePrams):
    class Meta:
        model = models.Event
        exclude = []
        widgets = {
            "evntc_id": forms.Select(attrs={"class": "chosen-select-contains"}),
            "perc_id": forms.Select(attrs={"class": "chosen-select-contains"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_id'].create_url = 'bio_diversity:create_team'


class EvntcForm(CreatePrams):
    class Meta:
        model = models.EventCode
        exclude = []


class FacicForm(CreatePrams):
    class Meta:
        model = models.FacilityCode
        exclude = []


class FecuForm(CreateDatePrams):
    class Meta:
        model = models.Fecundity
        exclude = []


class FeedForm(CreatePrams):
    class Meta:
        model = models.Feeding
        exclude = []


class FeedcForm(CreatePrams):
    class Meta:
        model = models.FeedCode
        exclude = []


class FeedmForm(CreatePrams):
    class Meta:
        model = models.FeedMethod
        exclude = []


class GrpForm(CreatePrams):
    class Meta:
        model = models.Group
        exclude = []


class GrpdForm(CreatePrams):
    class Meta:
        model = models.GroupDet
        exclude = []


class HeatForm(CreatePrams):
    class Meta:
        model = models.HeathUnit
        exclude = []
        widgets = {
            'inservice_date': forms.DateInput(attrs={"placeholder": "Click to select a date..", "class": "fp-date"})
        }


class HeatdForm(CreateDatePrams):
    class Meta:
        model = models.HeathUnitDet
        exclude = []


class HelpTextForm(forms.ModelForm):

    model = None

    class Meta:
        fields = "__all__"
        widgets = {
            'eng_text': forms.Textarea(attrs={"rows": 2}),
            'fra_text': forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clsmembers = [(cls[0], cls[0]) for cls in inspect.getmembers(models, inspect.isclass)]

        self.fields['model'] = forms.ChoiceField(choices=clsmembers)


HelpTextFormset = modelformset_factory(
    model=models.HelpText,
    form=HelpTextForm,
    extra=1,
)


class ImgForm(CreatePrams):
    class Meta:
        model = models.Image
        exclude = []


class ImgcForm(CreatePrams):
    class Meta:
        model = models.ImageCode
        exclude = []


class IndvForm(CreatePrams):
    class Meta:
        model = models.Individual
        exclude = []

    field_order = [
        'ufid',
        'pit_tag',
        'indv_valid',
        'grp_id',
        'spec_id',
        'stok_id',
        'coll_id',
        'comments',
    ]


class IndvdForm(CreatePrams):
    class Meta:
        model = models.IndividualDet
        exclude = []


class IndvtForm(CreateTimePrams):
    class Meta:
        model = models.IndTreatment
        exclude = []
        widgets = {}


class IndvtcForm(CreatePrams):
    class Meta:
        model = models.IndTreatCode
        exclude = []


class InstForm(CreatePrams):
    class Meta:
        model = models.Instrument
        exclude = []


class InstcForm(CreatePrams):
    class Meta:
        model = models.InstrumentCode
        exclude = []


class InstdForm(CreateDatePrams):
    class Meta:
        model = models.InstrumentDet
        exclude = []


class InstdcForm(CreatePrams):
    class Meta:
        model = models.InstDetCode
        exclude = []


class LocForm(CreatePrams):
    class Meta:
        model = models.Location
        exclude = []
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['loc_date'].widget = forms.HiddenInput()
        self.fields['loc_date'].required = False
        self.fields['start_date'] = forms.DateField(widget=forms.DateInput(
            attrs={"placeholder": "Click to select a date...", "class": "fp-date"}))
        self.fields['start_time'] = forms.CharField(required=False, widget=forms.DateInput(attrs={"placeholder": "Click to select a time...", "class": "fp-time"}))

    def save(self, commit=True):
        obj = super().save(commit=False)  # here the object is not commited in db
        if self.cleaned_data["start_time"]:
            start_time = datetime.strptime(self.cleaned_data["start_time"],
                                           '%H:%M').time().replace(tzinfo=pytz.UTC)
        else:
            start_time = datetime.min.time().replace(tzinfo=pytz.UTC)
        obj.loc_date = datetime.combine(self.cleaned_data["start_date"], start_time)
        obj.save()
        return obj


class LoccForm(CreatePrams):
    class Meta:
        model = models.LocCode
        exclude = []


class MatpForm(CreatePrams):
    class Meta:
        model = models.MatingPlan
        exclude = []


class MortForm(forms.Form):
    class Meta:
        model = models.MatingPlan
        exclude = []

    gender_choices = ((None, "---------"), ('Male', 'Male'), ('Female', 'Female'), ('Immature', 'Immature'))
    mort_date = forms.DateField(required=True, label=_("Date of Mortality"))
    perc_id = forms.ModelChoiceField(required=True, queryset=models.PersonnelCode.objects.filter(perc_valid=True), label=_("Personel"))
    created_date = forms.DateField(required=True)
    created_by = forms.CharField(required=True, max_length=32)
    indv_length = forms.DecimalField(required=False, max_digits=5, label=_("Individual Length (cm)"))
    indv_mass = forms.DecimalField(required=False, max_digits=5,  label=_("Individual Mass (g)"))
    indv_vial = forms.DecimalField(required=False, max_digits=5,  label=_("Individual Vial"))
    indv_gender = forms.ChoiceField(required=False, choices=gender_choices,  label=_("Individual Gender"))
    observations = forms.ModelMultipleChoiceField(required=False, queryset=models.AniDetSubjCode.objects.filter(anidc_id__name="Mortality Observation") | models.AniDetSubjCode.objects.filter(anidc_id__name="Animal Health"),  label=_("Observations"))
    indv_mort = forms.IntegerField(required=False, max_value=10000000)
    grp_mort = forms.IntegerField(required=False, max_value=10000000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_date'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['indv_mort'].widget = forms.HiddenInput()
        self.fields['grp_mort'].widget = forms.HiddenInput()
        self.fields['mort_date'].widget = forms.DateInput(attrs={"placeholder": "Click to select a date..",
                                                                 "class": "fp-date"})

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["mort_date"] = datetime.combine(cleaned_data["mort_date"], datetime.min.time()).replace(tzinfo=pytz.UTC)

        if not self.is_valid():
            return cleaned_data

        if cleaned_data["indv_mort"]:
            indv = models.Individual.objects.filter(pk=cleaned_data["indv_mort"]).get()
            indv.indv_valid = False
            indv.save()
            evnt = models.AniDetailXref.objects.filter(indv_id_id=cleaned_data["indv_mort"]).last().evnt_id
        else:
            evnt = models.AniDetailXref.objects.filter(grp_id_id=cleaned_data["grp_mort"]).last().evnt_id
            grp = models.Group.objects.filter(pk=cleaned_data["grp_mort"]).get()
            indv = models.Individual(grp_id=grp,
                                     spec_id=grp.spec_id,
                                     stok_id=grp.stok_id,
                                     coll_id=grp.coll_id,
                                     indv_year=grp.grp_year,
                                     indv_valid=False,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
            indv.clean()
            indv.save()
            cleaned_data["indv_mort"] = indv.pk

        mortality_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Mortality").get(),
                                      facic_id=evnt.facic_id,
                                      prog_id=evnt.prog_id,
                                      perc_id=cleaned_data["perc_id"],
                                      start_datetime=cleaned_data["mort_date"],
                                      end_datetime=cleaned_data["mort_date"],
                                      created_by=cleaned_data["created_by"],
                                      created_date=cleaned_data["created_date"],
                                      )
        try:
            mortality_evnt.clean()
            mortality_evnt.save()
        except (ValidationError, IntegrityError):
            mortality_evnt = models.Event.objects.filter(evntc_id=mortality_evnt.evntc_id,
                                                         facic_id=mortality_evnt.facic_id,
                                                         prog_id=mortality_evnt.prog_id,
                                                         start_datetime=mortality_evnt.start_datetime,
                                                         end_datetime=mortality_evnt.end_datetime,
                                                         ).get()
        cleaned_data["evnt_id"] = mortality_evnt

        anix = enter_anix(cleaned_data, indv_pk=cleaned_data["indv_mort"])
        if cleaned_data["grp_mort"]:
            anix_grp = enter_anix(cleaned_data, grp_pk=cleaned_data["grp_mort"])
            anix_both = enter_anix(cleaned_data, indv_pk=cleaned_data["indv_mort"], grp_pk=cleaned_data["grp_mort"])

        if cleaned_data["indv_length"]:
            enter_indvd(anix.pk, cleaned_data, cleaned_data["mort_date"], cleaned_data["indv_length"], "Length", None)
        if cleaned_data["indv_mass"]:
            enter_indvd(anix.pk, cleaned_data, cleaned_data["mort_date"], cleaned_data["indv_mass"], "Weight", None)
        if cleaned_data["indv_vial"]:
            enter_indvd(anix.pk, cleaned_data, cleaned_data["mort_date"], cleaned_data["indv_vial"], "Vial", None)
        if cleaned_data["indv_gender"]:
            enter_indvd(anix.pk, cleaned_data, cleaned_data["mort_date"], None, "Gender", cleaned_data["indv_gender"])

        if cleaned_data["observations"].count() != 0:
            for adsc in cleaned_data["observations"]:
                enter_indvd(anix.pk, cleaned_data, cleaned_data["mort_date"], None, adsc.anidc_id.name, adsc.name, None)


class OrgaForm(CreatePrams):
    class Meta:
        model = models.Organization
        exclude = []


class PairForm(CreateDatePrams):
    class Meta:
        model = models.Pairing
        exclude = []
        widgets = {
            "indv_id": forms.Select(attrs={"class": "chosen-select-contains"}),
        }


class PercForm(CreatePrams):
    class Meta:
        model = models.PersonnelCode
        exclude = []


class PrioForm(CreatePrams):
    class Meta:
        model = models.PriorityCode
        exclude = []


class ProgForm(CreateDatePrams):
    class Meta:
        model = models.Program
        exclude = []


class ProgaForm(CreatePrams):
    class Meta:
        model = models.ProgAuthority
        exclude = []


class ProtForm(CreateDatePrams):
    class Meta:
        model = models.Protocol
        exclude = []
        widgets = {
            "evntc_id": forms.Select(attrs={"class": "chosen-select-contains"}),
            "protc_id": forms.Select(attrs={"class": "chosen-select-contains"}),
        }


class ProtcForm(CreatePrams):
    class Meta:
        model = models.ProtoCode
        exclude = []


class ProtfForm(CreatePrams):
    class Meta:
        model = models.Protofile
        exclude = []


class QualForm(CreatePrams):
    class Meta:
        model = models.QualCode
        exclude = []


class RelcForm(CreatePrams):
    class Meta:
        model = models.ReleaseSiteCode
        exclude = []


class RiveForm(CreatePrams):
    class Meta:
        model = models.RiverCode
        exclude = []


class RoleForm(CreatePrams):
    class Meta:
        model = models.RoleCode
        exclude = []


class SampForm(CreatePrams):
    class Meta:
        model = models.Sample
        exclude = []


class SampcForm(CreatePrams):
    class Meta:
        model = models.SampleCode
        exclude = []


class SampdForm(CreatePrams):
    class Meta:
        model = models.SampleDet
        exclude = []


class SireForm(CreatePrams):
    class Meta:
        model = models.Sire
        exclude = []
        widgets = {
            "indv_id": forms.Select(attrs={"class": "chosen-select-contains"}),
        }


class SpwndForm(CreatePrams):
    class Meta:
        model = models.SpawnDet
        exclude = []


class SpwndcForm(CreatePrams):
    class Meta:
        model = models.SpawnDetCode
        exclude = []


class SpwnscForm(CreatePrams):
    class Meta:
        model = models.SpawnDetSubjCode
        exclude = []


class SpecForm(CreatePrams):
    class Meta:
        model = models.SpeciesCode
        exclude = []


class StokForm(CreatePrams):
    class Meta:
        model = models.StockCode
        exclude = []


class SubrForm(CreatePrams):
    class Meta:
        model = models.SubRiverCode
        exclude = []


class TankForm(CreatePrams):
    class Meta:
        model = models.Tank
        exclude = []


class TankdForm(CreateDatePrams):
    class Meta:
        model = models.TankDet
        exclude = []


class TeamForm(CreatePrams):
    class Meta:
        model = models.Team
        exclude = []


class TrayForm(CreatePrams):
    class Meta:
        model = models.Tray
        exclude = []


class TraydForm(CreateDatePrams):
    class Meta:
        model = models.TrayDet
        exclude = []


class TribForm(CreatePrams):
    class Meta:
        model = models.Tributary
        exclude = []


class TrofForm(CreatePrams):
    class Meta:
        model = models.Trough
        exclude = []


class TrofdForm(CreateDatePrams):
    class Meta:
        model = models.TroughDet
        exclude = []


class UnitForm(CreatePrams):
    class Meta:
        model = models.UnitCode
        exclude = []
