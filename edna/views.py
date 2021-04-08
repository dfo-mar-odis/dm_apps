import csv
from io import StringIO
import datetime as dt
import requests
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Value, TextField
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy, gettext as _

from lib.templatetags.custom_filters import nz
from shared_models.views import CommonTemplateView, CommonHardDeleteView, CommonFormsetView, CommonFormView, CommonDeleteView, CommonDetailView, \
    CommonCreateView, CommonUpdateView, CommonFilterView, CommonPopoutCreateView, CommonPopoutUpdateView, CommonPopoutDeleteView
from . import models, forms, filters, utils
from .mixins import LoginAccessRequiredMixin, eDNAAdminRequiredMixin
from .utils import in_edna_admin_group


class IndexTemplateView(LoginAccessRequiredMixin, CommonTemplateView):
    h1 = "home"
    active_page_name_crumb = "home"
    template_name = 'edna/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = in_edna_admin_group(self.request.user)
        return context


# REFERENCE TABLES #
####################

class FiltrationTypeFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage Fitlration Types"
    queryset = models.FiltrationType.objects.all()
    formset_class = forms.FiltrationTypeFormset
    success_url_name = "edna:manage_filtration_types"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_filtration_type"


class FiltrationTypeHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.FiltrationType
    success_url = reverse_lazy("edna:manage_filtration_types")


class DNAExtractionProtocolFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage DNA Extraction Protocols"
    queryset = models.DNAExtractionProtocol.objects.all()
    formset_class = forms.DNAExtractionProtocolFormset
    success_url_name = "edna:manage_dna_extraction_protocols"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_dna_extraction_protocol"


class DNAExtractionProtocolHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.DNAExtractionProtocol
    success_url = reverse_lazy("edna:manage_dna_extraction_protocols")


class TagFormsetView(eDNAAdminRequiredMixin, CommonFormsetView):
    template_name = 'edna/formset.html'
    h1 = "Manage Tags"
    queryset = models.Tag.objects.all()
    formset_class = forms.TagFormset
    success_url_name = "edna:manage_tags"
    home_url_name = "edna:index"
    delete_url_name = "edna:delete_tag"


class TagHardDeleteView(eDNAAdminRequiredMixin, CommonHardDeleteView):
    model = models.Tag
    success_url = reverse_lazy("edna:manage_tags")


# SPECIES #
###########

class SpeciesListView(eDNAAdminRequiredMixin, CommonFilterView):
    template_name = 'edna/list.html'
    filterset_class = filters.SpeciesFilter
    home_url_name = "edna:index"
    new_object_url = reverse_lazy("edna:species_new")
    row_object_url_name = row_ = "edna:species_detail"
    container_class = "container-fluid bg-light curvy"

    field_list = [
        {"name": 'tcommon|{}'.format("common name"), "class": "", "width": ""},
        {"name": 'formatted_scientific|{}'.format("scientific name"), "class": "", "width": ""},
    ]

    def get_queryset(self):
        return models.Species.objects.annotate(
            search_term=Concat('common_name_en', Value(" "), 'common_name_fr', Value(" "), 'scientific_name', output_field=TextField()))


class SpeciesUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Species
    form_class = forms.SpeciesForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("edna:species_list")}
    container_class = "container bg-light curvy"


class SpeciesCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Species
    form_class = forms.SpeciesForm
    success_url = reverse_lazy('edna:species_list')
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("edna:species_list")}
    container_class = "container bg-light curvy"


class SpeciesDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Species
    template_name = 'edna/species_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Species"), "url": reverse_lazy("edna:species_list")}
    container_class = "container bg-light curvy"
    field_list = [
        'tcommon|{}'.format("common name"),
        'formatted_scientific|{}'.format("scientific name"),
        'tsn',
        'aphia_id',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpeciesDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Species
    success_url = reverse_lazy('edna:species_list')
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container bg-light curvy"


# COLLECTIONS #
###############

class CollectionListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.Collection
    template_name = 'edna/list.html'
    filterset_class = filters.CollectionFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:collection_detail"
    new_object_url = reverse_lazy("edna:collection_new")
    new_btn_text = gettext_lazy("Add a New Collection")
    container_class = "container-fluid bg-light curvy"
    field_list = [
        {"name": 'fiscal_year', "class": "", "width": ""},
        {"name": 'region', "class": "", "width": ""},
        {"name": 'name', "class": "", "width": ""},
        {"name": 'location_description', "class": "", "width": ""},
        {"name": 'province', "class": "", "width": ""},
        {"name": 'sample_count|{}'.format(_("sample count")), "class": "", "width": ""},
    ]


class CollectionUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Collection
    form_class = forms.CollectionForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:collection_detail", args=[self.get_object().id])}


class CollectionCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Collection
    form_class = forms.CollectionForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container bg-light curvy"


class CollectionDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Collection
    template_name = 'edna/collection_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container bg-light curvy"

    def get_field_list(self):
        return utils.get_collection_field_list(self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_field_list = [
            'unique_sample_identifier',
            'datetime',
            'site_identifier',
            'coordinates',
            # 'observation_count|{}'.format(_("lobster count")),
        ]
        context["sample_field_list"] = sample_field_list
        return context


class CollectionDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Collection
    success_url = reverse_lazy('edna:collection_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container bg-light curvy"
    grandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:collection_detail", args=[self.get_object().id])}




class ImportSamplesView(eDNAAdminRequiredMixin, CommonFormView):
    form_class = forms.FileImportForm
    template_name = 'edna/sample_import_form.html'
    home_url_name = "index"
    grandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    h1 = ' '

    def get_parent_crumb(self):
        return {"title": self.get_collection(), "url": reverse("edna:collection_detail", args=[self.get_collection().id])}

    def get_collection(self):
        return get_object_or_404(models.Collection, pk=self.kwargs.get("pk"))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        example_obj = list()
        url = "http://" + get_current_site(self.request).domain + static("edna/sample_import_template.csv")
        r = requests.get(url)
        csv_reader = csv.DictReader(r.text.splitlines())
        for row in csv_reader:
            example_obj.append(row)
        context["example_obj"] = example_obj
        return context

    def form_valid(self, form):
        my_object = self.get_collection()
        temp_file = form.files['temp_file']
        temp_file.seek(0)
        csv_reader = csv.DictReader(StringIO(temp_file.read().decode('utf-8')))
        for row in csv_reader:
            unique_sample_identifier = row["unique_sample_identifier"]
            site_identifier = row["site_identifier"]
            site_description = row["site_description"]
            samplers = row["samplers"]
            datetime = dt.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%S")
            latitude = row["latitude"]
            longitude = row["longitude"]
            comments = row["comments"]

            sample, create = models.Sample.objects.get_or_create(unique_sample_identifier=unique_sample_identifier, collection=my_object)
            sample.site_identifier = site_identifier
            sample.site_description = site_description
            sample.samplers = samplers
            sample.datetime = datetime
            sample.latitude = latitude
            sample.longitude = longitude
            sample.comments = comments
            sample.save()
        return HttpResponseRedirect(self.get_parent_crumb()["url"])




# FILES #
#########

class FileCreateView(eDNAAdminRequiredMixin, CommonPopoutCreateView):
    model = models.File
    form_class = forms.FileForm
    is_multipart_form_data = True

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.collection_id = self.kwargs['collection']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class FileUpdateView(eDNAAdminRequiredMixin, CommonPopoutUpdateView):
    model = models.File
    form_class = forms.FileForm
    is_multipart_form_data = True


class FileDeleteView(eDNAAdminRequiredMixin, CommonPopoutDeleteView):
    model = models.File


# SAMPLES #
###########

class SampleCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    container_class = "container bg-light curvy"
    grandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}

    def get_cancel_url(self):
        return self.get_parent_crumb().get("url")

    def get_initial(self):
        return dict(add_another=True, collection_date=timezone.now())

    def get_collection(self):
        return get_object_or_404(models.Collection, pk=self.kwargs.get("collection"))

    def get_parent_crumb(self):
        return {"title": self.get_collection(), "url": reverse("edna:collection_detail", args=[self.get_collection().id])}

    def get_success_url(self):
        return self.get_parent_crumb()["url"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        collection = self.get_collection()
        obj.collection = collection
        obj.save()
        if form.cleaned_data.get("add_another", False):
            return HttpResponseRedirect(reverse("edna:sample_new", args=[collection.id]))
        else:
            return HttpResponseRedirect(self.get_success_url())


class SampleUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.Sample
    form_class = forms.SampleForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    greatgrandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("edna:sample_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().collection, "url": reverse_lazy("edna:collection_detail", args=[self.get_object().collection.id])}


class SampleDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.Sample
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container bg-light curvy"
    home_url_name = "edna:index"
    greatgrandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse_lazy("edna:sample_detail", args=[self.get_object().id])}

    def get_grandparent_crumb(self):
        return {"title": self.get_object().collection, "url": reverse_lazy("edna:collection_detail", args=[self.get_object().collection.id])}

    def get_success_url(self):
        return self.get_grandparent_crumb().get("url")


class SampleDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.Sample
    template_name = 'edna/sample_detail.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Collections"), "url": reverse_lazy("edna:collection_list")}
    container_class = "container bg-light curvy"
    field_list = [
        'unique_sample_identifier',
        'site_identifier',
        'site_description',
        'samplers',
        'datetime',
        'coordinates',
        'comments',
    ]

    def get_parent_crumb(self):
        return {"title": self.get_object().collection, "url": reverse("edna:collection_detail", args=[self.get_object().collection.id])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # section_field_list = [
        #     'interval',
        #     'depth_ft',
        #     'substrate_profile|{}'.format(_("substrate profile")),
        #     'comment',
        # ]
        # context["section_field_list"] = section_field_list
        # observation_field_list = [
        #     'id',
        #     'sex_special_display|{}'.format("sex"),
        #     'egg_status_special_display|{}'.format("egg status"),
        #     'carapace_length_mm',
        #     'certainty_rating_special_display|{}'.format("length certainty"),
        #     'comment',
        # ]
        # context["observation_field_list"] = observation_field_list
        # context["random_observation"] = models.Observation.objects.first()
        return context


# FILTRATION BATCHES #
######################

class FiltrationBatchListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.FiltrationBatch
    template_name = 'edna/list.html'
    filterset_class = filters.FiltrationBatchFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:filtration_batch_detail"
    new_object_url = reverse_lazy("edna:filtration_batch_new")
    new_btn_text = gettext_lazy("Add a New Filtration Batch")
    container_class = "container-fluid bg-light curvy"
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'operators', "class": "", "width": ""},
        {"name": 'comments', "class": "", "width": ""},
    ]


class FiltrationBatchUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.FiltrationBatch
    form_class = forms.FiltrationBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:filtration_batch_detail", args=[self.get_object().id])}


class FiltrationBatchCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.FiltrationBatch
    form_class = forms.FiltrationBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    container_class = "container bg-light curvy"


class FiltrationBatchDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.FiltrationBatch
    template_name = 'edna/filtration_batch_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}
    container_class = "container-fluid"
    field_list = utils.get_batch_field_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_field_list = [
            'unique_sample_identifier',
            'datetime',
            'site_identifier',
            'coordinates',
            # 'observation_count|{}'.format(_("lobster count")),
        ]
        context["sample_field_list"] = sample_field_list
        return context


class FiltrationBatchDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.FiltrationBatch
    success_url = reverse_lazy('edna:filtration_batch_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container bg-light curvy"
    grandparent_crumb = {"title": gettext_lazy("Filtration Batches"), "url": reverse_lazy("edna:filtration_batch_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:filtration_batch_detail", args=[self.get_object().id])}


# EXTRACTION BATCHES #
######################

class ExtractionBatchListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.ExtractionBatch
    template_name = 'edna/list.html'
    filterset_class = filters.ExtractionBatchFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:extraction_batch_detail"
    new_object_url = reverse_lazy("edna:extraction_batch_new")
    new_btn_text = gettext_lazy("Add a New Extraction Batch")
    container_class = "container-fluid bg-light curvy"
    h1 = gettext_lazy("DNA Extraction Batches")
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'operators', "class": "", "width": ""},
        {"name": 'comments', "class": "", "width": ""},
    ]


class ExtractionBatchUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.ExtractionBatch
    form_class = forms.ExtractionBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:extraction_batch_detail", args=[self.get_object().id])}


class ExtractionBatchCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.ExtractionBatch
    form_class = forms.ExtractionBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    container_class = "container bg-light curvy"


class ExtractionBatchDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.ExtractionBatch
    template_name = 'edna/extraction_batch_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}
    container_class = "container bg-light curvy"
    field_list = utils.get_batch_field_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_field_list = [
            'unique_sample_identifier',
            'datetime',
            'site_identifier',
            'coordinates',
            # 'observation_count|{}'.format(_("lobster count")),
        ]
        context["sample_field_list"] = sample_field_list
        return context


class ExtractionBatchDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.ExtractionBatch
    success_url = reverse_lazy('edna:extraction_batch_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container bg-light curvy"
    grandparent_crumb = {"title": gettext_lazy("Extraction Batches"), "url": reverse_lazy("edna:extraction_batch_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:extraction_batch_detail", args=[self.get_object().id])}


# PCR BATCHES #
######################

class PCRBatchListView(eDNAAdminRequiredMixin, CommonFilterView):
    model = models.PCRBatch
    template_name = 'edna/list.html'
    filterset_class = filters.PCRBatchFilter
    home_url_name = "edna:index"
    row_object_url_name = "edna:pcr_batch_detail"
    new_object_url = reverse_lazy("edna:pcr_batch_new")
    new_btn_text = gettext_lazy("Add a New PCR Batch")
    container_class = "container-fluid bg-light curvy"
    h1 = gettext_lazy("qPCR Batches")
    field_list = [
        {"name": 'id', "class": "", "width": ""},
        {"name": 'datetime', "class": "", "width": ""},
        {"name": 'operators', "class": "", "width": ""},
        {"name": 'comments', "class": "", "width": ""},
    ]


class PCRBatchUpdateView(eDNAAdminRequiredMixin, CommonUpdateView):
    model = models.PCRBatch
    form_class = forms.PCRBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    grandparent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    container_class = "container bg-light curvy"

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:pcr_batch_detail", args=[self.get_object().id])}


class PCRBatchCreateView(eDNAAdminRequiredMixin, CommonCreateView):
    model = models.PCRBatch
    form_class = forms.PCRBatchForm
    template_name = 'edna/form.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    container_class = "container bg-light curvy"


class PCRBatchDetailView(eDNAAdminRequiredMixin, CommonDetailView):
    model = models.PCRBatch
    template_name = 'edna/pcr_batch_detail.html'
    home_url_name = "edna:index"
    parent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}
    container_class = "container bg-light curvy"
    field_list = utils.get_batch_field_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_field_list = [
            'unique_sample_identifier',
            'datetime',
            'site_identifier',
            'coordinates',
            # 'observation_count|{}'.format(_("lobster count")),
        ]
        context["sample_field_list"] = sample_field_list
        return context


class PCRBatchDeleteView(eDNAAdminRequiredMixin, CommonDeleteView):
    model = models.PCRBatch
    success_url = reverse_lazy('edna:pcr_batch_list')
    home_url_name = "edna:index"
    success_message = 'The functional group was successfully deleted!'
    template_name = 'edna/confirm_delete.html'
    container_class = "container bg-light curvy"
    grandparent_crumb = {"title": gettext_lazy("PCR Batches"), "url": reverse_lazy("edna:pcr_batch_list")}

    def get_parent_crumb(self):
        return {"title": self.get_object(), "url": reverse("edna:pcr_batch_detail", args=[self.get_object().id])}


# REPORTS #
###########

class ReportSearchFormView(eDNAAdminRequiredMixin, CommonFormView):
    template_name = 'edna/report_search.html'
    form_class = forms.ReportSearchForm
    h1 = gettext_lazy("eDNA Reports")

    def form_valid(self, form):
        report = int(form.cleaned_data["report"])
        year = nz(form.cleaned_data["year"], "None")
        # if report == 1:
        #     return HttpResponseRedirect(reverse("edna:sample_log_report") + f"?year={year}")
        # else:
        messages.error(self.request, "Report is not available. Please select another report.")
        return HttpResponseRedirect(reverse("edna:reports"))

#
# @login_required()
# def sample_log_report(request):
#     year = None if not request.GET.get("year") or request.GET.get("year") == "None" else int(request.GET.get("year"))
#     file_url = reports.generate_sample_log(year=year)
#
#     if os.path.exists(file_url):
#         with open(file_url, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = f'inline; filename="sample log ({timezone.now().strftime("%Y-%m-%d")}).xlsx"'
#
#             return response
#     raise Http404
