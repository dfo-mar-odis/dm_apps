from django.db import models
# from django.db.models import AutoField
from django.utils.translation import gettext_lazy as _

from shared_models import models as shared_models
from projects import models as project_models

from django.core.validators import MaxValueValidator, MaxLengthValidator, EmailValidator


# ----------------------------------------------------------------------------------------------------
#
class Lookup(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_fr = models.CharField(max_length=255, unique=True)

    description_en = models.TextField(null=True, blank=True)
    description_fr = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}/{}".format(self.name_en, self.name_fr)

    class Meta:
        abstract = True


# ----------------------------------------------------------------------------------------------------
# Create models for contacts
#
class CohHonorific(shared_models.Lookup):
    pass


class CotType(shared_models.Lookup):
    pass


class LanLanguage(shared_models.Lookup):
    pass


class NotNotificationPreference(shared_models.Lookup):
    pass


class RolRole(shared_models.Lookup):
    pass


class SecSector(shared_models.Lookup):
    pass


class CotStatus(shared_models.Lookup):
    pass


class CotExpertise(shared_models.Lookup):
    pass


class ConContact(models.Model):
    honorific = models.ForeignKey(CohHonorific, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  verbose_name=_("Honorific"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    affiliation = models.CharField(max_length=100, verbose_name=_("Affiliation"))
    region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name="region_name", verbose_name=_("Region"))
    sector = models.ForeignKey(SecSector, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Sector"))
    role = models.ForeignKey(RolRole, null=True, blank=True, on_delete=models.DO_NOTHING,
                             help_text=_("Indicates permissions i.e. regional coordinator, regional science adviser, "
                                         "regional admin, director, etc."),
                             verbose_name=_("Role"))
    job_title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Job Title"))
    language = models.ForeignKey(LanLanguage, on_delete=models.DO_NOTHING, verbose_name=_("Language"))
    contact_type = models.ForeignKey(CotType, on_delete=models.DO_NOTHING, verbose_name=_("Contact Type"))
    status = models.ForeignKey(CotStatus, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Status"))
    notification_preference = models.ForeignKey(NotNotificationPreference, models.DO_NOTHING,
                                                verbose_name=_("Communication Preference"))
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name=_("Phone"))
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("E-mail"))

    expertise = models.ForeignKey(CotExpertise, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  verbose_name=_("Expertise"))
    cc_grad = models.BooleanField(null=True, blank=True, verbose_name=_("Chair Course Graduate"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)

    class Meta:
        # abstract = True
        ordering = ['last_name']


# ----------------------------------------------------------------------------------------------------
# Create models for meetings
#
class FilFile(models.Model):
    file = models.BooleanField()

    def __str__(self):
        return "{}".format(self.file)


class MftMeetingFileType(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return "{}".format(self.name)


class SttStatus(shared_models.Lookup):
    pass


class ScpScope(shared_models.Lookup):
    pass


class AptAdvisoryProcessType(shared_models.Lookup):
    pass


class LocLocationProv(shared_models.Lookup):
    pass


class LocLocationCity(shared_models.Lookup):
    pass


class MdfMeetingDocsRef(shared_models.Lookup):
    pass


class MepMeetingExpectedPublication(shared_models.Lookup):
    pass


class MccMeetingCostCategory(shared_models.Lookup):
    pass


class MeqQuarter(shared_models.Lookup):
    pass


class MemMeetingMonth(shared_models.Lookup):
    pass


# class MeqQuarter(shared_models.Lookup):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


# class MemMeetingMonth(shared_models.Lookup):
#     quarter = models.ForeignKey(MeqQuarter, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#        return self.name


class MetMeeting(models.Model):
    title_en = models.CharField(max_length=255, verbose_name=_("Meeting Title (English)"))
    title_fr = models.CharField(max_length=255, verbose_name=_("Meeting Title (French)"))
    status = models.ForeignKey(SttStatus, on_delete=models.DO_NOTHING, verbose_name=_("Meeting Status"))
    status_notes = models.TextField(null=True, blank=True, verbose_name=_("Status Notes"))
    quarter = models.ForeignKey(MeqQuarter, on_delete=models.DO_NOTHING, verbose_name=_("Meeting Quarter"))
    month = models.ForeignKey(MemMeetingMonth, on_delete=models.DO_NOTHING, verbose_name=_("Meeting Month"))
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Start Date"),
                                  help_text=_("Format: YYYY-MM-DD"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"),
                                help_text=_("Format: YYYY-MM-DD"))
    range_en = models.CharField(max_length=255, verbose_name=_("Meeting Date Range (English)"))
    range_fr = models.CharField(max_length=255, verbose_name=_("Meeting Date Range (French)"))
    location_prov = models.ForeignKey(LocLocationProv, on_delete=models.DO_NOTHING,
                                      verbose_name=_("Meeting Location Province"))
    location_city = models.ForeignKey(LocLocationCity, on_delete=models.DO_NOTHING,
                                      verbose_name=_("Meeting Location City"))
    scope = models.ForeignKey(ScpScope, on_delete=models.DO_NOTHING, verbose_name=_("Scope"))
    process_type = models.ForeignKey(AptAdvisoryProcessType, on_delete=models.DO_NOTHING,
                                     verbose_name=_("Type of Advisory Process"))
    # lead_region = models.ForeignKey(shared_models.Region, blank=True, on_delete=models.DO_NOTHING,
    #                                 verbose_name=_("Lead Region"))
    lead_region = models.ForeignKey(shared_models.Region, blank=True, on_delete=models.DO_NOTHING,
                                    verbose_name=_("Lead Region"))
    other_region = models.ManyToManyField(shared_models.Region, blank=True, related_name="other_regions",
                                          verbose_name=_("Other Regions"))
    # exp_publication = models.ForeignKey(MepMeetingExpectedPublication, null=True, blank=True,
    #                                     on_delete=models.DO_NOTHING, verbose_name=_("Expected Publication(s)"))
    exp_publication = models.ManyToManyField(MepMeetingExpectedPublication, blank=True, related_name="exp_publication",
                                             verbose_name=_("Expected Publication(s)"))
    # other_region = models.ManyToManyField(shared_models.Region, blank=True, related_name="other_regions",
    #                                       verbose_name=_("Other Regions"))
    chair = models.ManyToManyField(ConContact, blank=True, related_name="chairs", verbose_name=_("Chair(s)"))
    csas_contact = models.ManyToManyField(ConContact, blank=True, related_name="csas_contacts",
                                          verbose_name=_("CSAS Contact(s)"))
    program_contact = models.ManyToManyField(ConContact, blank=True, related_name="program_contacts",
                                             verbose_name=_("Program Contact(s)"))
    #
    # Yongcun: before it has been published, how could it be linked to PubPublication model, it doesn't exit in database
    #          Also, how can a user chose multiple publications
    #

    chair_comments = models.TextField(null=True, blank=True, verbose_name=_("Chair Comments"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"),
                                   help_text=_("Description of the meeting for reporting to senior management"))

    def __str__(self):
        return "{}".format(self.title_en)

    class Meta:
        ordering = ['-id']


class MedMeetingDocs(models.Model):
    meeting = models.ManyToManyField(MetMeeting, blank=True, related_name="meeting_docs", verbose_name=_('Meeting'))
    # meeting = models.OneToOneField(MetMeeting, on_delete=models.DO_NOTHING, related_name="meeting_doc", primary_key=True)
    pub_type = models.ForeignKey(MdfMeetingDocsRef, blank=True, on_delete=models.DO_NOTHING,
                                 verbose_name=_("Publication Type"))
    status = models.CharField(max_length=255, default='NA', verbose_name=_("Status"))
    due_date = models.DateField(null=True, blank=True, default='0001-01-01', help_text=_("Format: YYYY-MM-DD"),
                                verbose_name=_("Date Submitted"))
    date_posted = models.DateField(null=True, blank=True, default='0001-01-01', help_text=_("Format: YYYY-MM-DD"),
                                   verbose_name=_("Posted Date"))
    link = models.CharField(max_length=255, default='NA', verbose_name=_("Link"))
    confirmed = models.BooleanField(default=False)


class MetMeetingDFOPars(models.Model):
    # meeting = models.ForeignKey(to=MetMeeting, on_delete=models.CASCADE)
    meeting = models.ManyToManyField(MetMeeting, blank=True, related_name="meetingDFO", verbose_name=_('Meeting'))
    name = models.ManyToManyField(ConContact, blank=True, related_name="name_DFO", verbose_name=_("Name"))
    role = models.CharField(max_length=255, verbose_name=_("Role"))
    time = models.CharField(max_length=255, verbose_name=_("Time (Weeks)"))
    cost_category = models.CharField(max_length=255, verbose_name=_("Cost Category"))
    funding_source = models.CharField(max_length=255, verbose_name=_("Funding Source"))
    total_salary = models.CharField(max_length=255, verbose_name=_("Total Salary Amount"))


class MetMeetingOtherPars(models.Model):
    # meeting = models.ForeignKey(to=MetMeeting, on_delete=models.CASCADE)
    meeting = models.ManyToManyField(MetMeeting, blank=True, related_name="meetingOther", verbose_name=_('Meeting'))
    name = models.ManyToManyField(ConContact, blank=True, related_name="name_other", verbose_name=_("Name"))
    role = models.CharField(max_length=255, verbose_name=_("Role"))
    affiliation = models.CharField(max_length=255, verbose_name=_("Affiliation"))
    invited = models.BooleanField(verbose_name=_("Invited"))
    attended = models.BooleanField(verbose_name=_("Attended"))


class MocMeetingOMCosts(models.Model):
    meeting = models.ForeignKey(MetMeeting, on_delete=models.DO_NOTHING, related_name="meeting_costs",
                                verbose_name=_("Meeting"))
    category = models.ForeignKey(MccMeetingCostCategory, blank=False, on_delete=models.DO_NOTHING,
                                 verbose_name=_("Cost Category"), default=1)
    # categories (hospitality, travel, venue, interpretation, office, rentals, contractors, planning)
    description = models.CharField(max_length=255, verbose_name=_("Description"), default="")
    funding = models.CharField(max_length=255, verbose_name=_("Funding Source"), default="")
    total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Total O&M Amount"), default=0)

    def __str__(self):
        return "{}".format(self.meeting)


class MemMeetingMedia(models.Model):
    meeting = models.ManyToManyField(MetMeeting, blank=True, related_name="meeting_media", verbose_name=_('Meeting'))
    # meeting = models.OneToOneField(MetMeeting, on_delete=models.DO_NOTHING, primary_key=True)
    media_attention = models.BooleanField(default=False, verbose_name=_("Is Media Attention Anticipated"))
    media_attention_yes = models.TextField(null=True, blank=True, verbose_name=_("Why Media Attention Anticipated"))
    media_attention_no = models.TextField(null=True, blank=True, verbose_name=_("Why Media Attention Not Anticipated"))
    media_bullets = models.CharField(max_length=255, verbose_name=_("Media Bullets (ADM Summary Package)"))
    media_lines = models.CharField(max_length=255, verbose_name=_("Media Lines (Meeting/Publication)"))


class MecMeetingContact(models.Model):
    meeting = models.ForeignKey(MetMeeting, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(ConContact, on_delete=models.DO_NOTHING)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.meeting)


class OmCost(models.Model):
    amount = models.DecimalField(decimal_places=10, max_digits=20)
    funding_source = models.ForeignKey(project_models.FundingSource, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(project_models.OMCategory, on_delete=models.DO_NOTHING)

    description = models.TextField()

    def __str__(self):
        return "{}".format(self.pk)


class PsePublicationSeries(shared_models.Lookup):
    pass

    # def __str__(self):
    #     return "{}".format(self.pk)


class MefMeetingFile(models.Model):
    meeting = models.ForeignKey(MetMeeting, on_delete=models.DO_NOTHING)
    file_en = models.ForeignKey(FilFile, on_delete=models.DO_NOTHING, related_name="file_en")
    file_fr = models.ForeignKey(FilFile, on_delete=models.DO_NOTHING, related_name="file_fr")
    document_type = models.ForeignKey(MftMeetingFileType, on_delete=models.DO_NOTHING)
    date_submitted = models.DateField(blank=True, null=True, verbose_name=_("Date Submitted"))
    date_posted = models.DateField(blank=True, null=True, verbose_name=_("Date Postted"))

    def __str__(self):
        return "{}".format(self.meeting)


class MerOtherRegion(models.Model):
    meeting = models.ForeignKey(MetMeeting, on_delete=models.DO_NOTHING)
    # region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING)
    region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}".format(self.meeting)


class MomMeetingOmCost(models.Model):
    met_id = models.ForeignKey(MetMeeting, on_delete=models.DO_NOTHING)
    om_id = models.ForeignKey(OmCost, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}".format(self.pk)


# ----------------------------------------------------------------------------------------------------
# Create models for publications
#
class PseSeries(shared_models.Lookup):
    name = models.CharField(max_length=50)


class KeyKeywords(shared_models.Lookup):
    name = models.CharField(max_length=100)


class PusPublicationStatus(shared_models.Lookup):
    pass


class PtsPublicationTransStatus(shared_models.Lookup):
    pass


class PtlPublicationTargetLanguage(shared_models.Lookup):
    pass


class PurPublicationUrgentRequest(shared_models.Lookup):
    pass


class PccPublicationCostCategory(shared_models.Lookup):
    pass


class PccPublicationComResultsCategory(shared_models.Lookup):
    pass


class PubPublication(models.Model):
    series = models.ForeignKey(PsePublicationSeries, blank=True, on_delete=models.DO_NOTHING,
                               verbose_name=_("Series"))
    lead_region = models.ForeignKey(shared_models.Region, blank=True, on_delete=models.DO_NOTHING,
                                    verbose_name=_("Lead Region"))
    # lead_region = models.ForeignKey(shared_models.Region, blank=True, on_delete=models.DO_NOTHING,
    #                                 verbose_name=_("Lead Region"))
    title_en = models.CharField(max_length=255, verbose_name=_("Title (English)"))
    title_fr = models.CharField(max_length=255, verbose_name=_("Title (French)"))
    title_in = models.CharField(max_length=255, verbose_name=_("Title (Inuktitut)"))
    pub_year = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(9999)],
                                           verbose_name=_("Publication Year"))
    lead_author = models.ForeignKey(ConContact, null=True, blank=True, on_delete=models.DO_NOTHING,
                                    verbose_name=_("Lead Author"))
    other_author = models.ManyToManyField(ConContact, blank=True, related_name="other_authors",
                                          verbose_name=_("Other Author(s)"))
    pub_num = models.CharField(default="NA", max_length=25, verbose_name=_("Publication Number"))
    pages = models.IntegerField(null=True, blank=True, verbose_name=_("Pages"))
    pdf_size = models.IntegerField(null=True, blank=True, verbose_name=_("PDF Size"))
    keywords = models.CharField(default="NA", max_length=25, verbose_name=_("Keywords"))
    citation = models.TextField(null=True, blank=True, verbose_name=_("Citation"))
    client = models.ManyToManyField(ConContact, blank=True, related_name="clients",
                                    verbose_name=_("Client(s)"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def __str__(self):
        return "{}/{}".format(self.title_en, self.title_fr)

    class Meta:
        ordering = ['-id']


class PubPublicationStatus(models.Model):
    publication = models.ManyToManyField(PubPublication, blank=True, related_name="pub_status",
                                         verbose_name=_('Publication'))
    # publication = models.OneToOneField(PubPublication, on_delete=models.DO_NOTHING, primary_key=True,
    #                                    related_name="pub_status", verbose_name=_('Publication'))
    date_due = models.DateField(null=True, blank=True, verbose_name=_("Date Due"))
    status = models.ForeignKey(PusPublicationStatus, on_delete=models.DO_NOTHING, verbose_name=_("Status"))
    status_comments = models.TextField(null=True, blank=True, verbose_name=_("Status Comments"))
    date_submitted = models.DateField(null=True, blank=True, verbose_name=_("Date Submitted by Author"))
    submitted_by = models.ManyToManyField(ConContact, blank=True, related_name="submitted_by",
                                          verbose_name=_("Submitted By"))
    date_appr_by_chair = models.DateField(null=True, blank=True, verbose_name=_("Date Approved by Chair"))
    appr_by_chair = models.ManyToManyField(ConContact, blank=True, related_name="appr_by_chair",
                                           verbose_name=_("Approved By (Chair)"))
    data_appr_by_CSAS = models.DateField(null=True, blank=True, verbose_name=_("Date Approved by CSAS"))
    appr_by_CSAS = models.ManyToManyField(ConContact, blank=True, related_name="appr_by_CSAS",
                                          verbose_name=_("Approved By (CSAS Contact)"))
    date_appr_by_dir = models.DateField(null=True, blank=True, verbose_name=_("Date Approved by Director"))
    appr_by_dir = models.ManyToManyField(ConContact, blank=True, related_name="appr_by_dir",
                                         verbose_name=_("Approved By Director"))
    date_num_req = models.DateField(null=True, blank=True, verbose_name=_("Date Number Requested"))
    date_doc_submitted = models.DateField(null=True, blank=True, verbose_name=_("Date Document Submitted to CSAS"))
    date_pdf_proof = models.DateField(null=True, blank=True, verbose_name=_("Date PDF Proof Sent to Author"))
    appr_by = models.ManyToManyField(ConContact, blank=True, related_name="appr_by",
                                     verbose_name=_("Approved by (PDF Proof)"))
    date_anti = models.DateField(null=True, blank=True, verbose_name=_("Date of Anticipated Posting"))
    date_posted = models.DateField(null=True, blank=True, verbose_name=_("Date Posted"))
    date_modify = models.DateField(null=True, blank=True, verbose_name=_("Date Modified"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))


class PubPublicationTransInfo(models.Model):
    publication = models.ManyToManyField(PubPublication, blank=True, related_name="pub_trans_info",
                                         verbose_name=_('Publication'))
    # publication = models.OneToOneField(PubPublication, on_delete=models.DO_NOTHING, primary_key=True)
    trans_status = models.ForeignKey(PtsPublicationTransStatus, on_delete=models.DO_NOTHING,
                                     verbose_name=_("Translation Status"))
    date_to_trans = models.DateField(null=True, blank=True, verbose_name=_("Date Sent to Translation"))
    client_ref_num = models.CharField(default="NA", max_length=255, verbose_name=_("Client Reference Number"))
    target_lang = models.ForeignKey(PtlPublicationTargetLanguage, on_delete=models.DO_NOTHING,
                                    verbose_name=_("Target Language"))
    trans_ref_num = models.CharField(default="NA", max_length=255, verbose_name=_("Translator Reference Number"))
    urgent_req = models.ForeignKey(PurPublicationUrgentRequest, on_delete=models.DO_NOTHING,
                                   verbose_name=_("Urgent Request"))
    date_fr_trans = models.DateField(null=True, blank=True, verbose_name=_("Date Back from Translation"))
    invoice_num = models.CharField(default="NA", max_length=255, verbose_name=_("Invoice Number"))
    attach = models.CharField(default="NA", max_length=255, verbose_name=_("Attachment(s)"))
    trans_note = models.TextField(null=True, blank=True, verbose_name=_("Translation Notes"))


class PubPublicationDocLocation(models.Model):
    publication = models.ManyToManyField(PubPublication, blank=True, related_name="pub_doc_location",
                                         verbose_name=_('Publication'))
    # publication = models.OneToOneField(PubPublication, on_delete=models.DO_NOTHING, primary_key=True)
    p1 = models.CharField(max_length=1, blank=True, verbose_name=_(""))
    attach_en_file = models.CharField(default="NA", max_length=255, verbose_name=_("Attachment (English) File"))
    attach_en_size = models.CharField(default="NA", max_length=255, verbose_name=_("Attachment (English) Size"))
    attach_fr_file = models.CharField(default="NA", max_length=255, verbose_name=_("Attachment (French) File"))
    attach_fr_size = models.CharField(default="NA", max_length=255, verbose_name=_("Attachment (French) Size"))

    url_e_file = models.URLField(_("URL (English)"), max_length=255, db_index=True, unique=True, blank=True)
    url_e_size = models.CharField(default="NA", max_length=255, verbose_name=_("URL (English) Size"))
    url_f_file = models.URLField(_("URL (French)"), max_length=255, db_index=True, unique=True, blank=True)
    url_f_size = models.CharField(default="NA", max_length=255, verbose_name=_("URL (French) Size"))

    dev_link_e_file = models.URLField(_("Dev Link (English)"), max_length=255, db_index=True, unique=True, blank=True)
    dev_link_e_size = models.CharField(default="NA", max_length=255, verbose_name=_("Dev Link (English) Size"))
    dev_link_f_file = models.URLField(_("Dev Link (French)"), max_length=255, db_index=True, unique=True, blank=True)
    dev_link_f_size = models.CharField(default="NA", max_length=255, verbose_name=_("Dev Link (French) Size"))

    ekme_gcdocs_e_file = models.CharField(default="NA", max_length=255, verbose_name=_("EKME# GCDocs (English)"))
    ekme_gcdocs_e_size = models.CharField(default="NA", max_length=255, verbose_name=_("EKME# GCDocs (English) Size"))
    ekme_gcdocs_f_file = models.CharField(default="NA", max_length=255, verbose_name=_("EKME# GCDocs (French)"))
    ekme_gcdocs_f_size = models.CharField(default="NA", max_length=255, verbose_name=_("EKME# GCDocs (French) Size"))

    lib_cat_e_file = models.CharField(default="NA", max_length=255, verbose_name=_("Library Catalogue # (English)"))
    lib_cat_e_size = models.CharField(default="NA", max_length=255, verbose_name=_("Library Catalogue # (English) Size"))
    lib_cat_f_file = models.CharField(default="NA", max_length=255, verbose_name=_("Library Catalogue # (French)"))
    lib_cat_f_size = models.CharField(default="NA", max_length=255, verbose_name=_("Library Catalogue # (French) Size"))

    lib_link_e_file = models.URLField(_("Library Link (English)"), max_length=255, db_index=True, unique=True, blank=True)
    lib_link_e_size = models.CharField(default="NA", max_length=255, verbose_name=_("Library Link (English) Size"))
    lib_link_f_file = models.URLField(_("Library Link (French)"), max_length=255, db_index=True, unique=True, blank=True)
    lib_link_f_size = models.CharField(default="NA", max_length=255, verbose_name=_("Library Link (French) Size"))


class PubPublicationOMCosts(models.Model):
    Publication = models.ForeignKey(PubPublication, on_delete=models.DO_NOTHING, related_name="publication_costs",
                                    verbose_name=_("Publication"))
    # publication = models.OneToOneField(PubPublication, on_delete=models.DO_NOTHING, primary_key=True,
    #                                    related_name="publication_costs")
    category = models.ForeignKey(PccPublicationCostCategory, blank=False, on_delete=models.DO_NOTHING,
                                 verbose_name=_("Publication Category"), default=1)
    # p1 = models.CharField(max_length=1, blank=True, verbose_name=_(""))
    trans_funding = models.CharField(default="NA", max_length=255,
                                     verbose_name=_("Translation Funding Source (e.g. sector)"))
    trans_code = models.CharField(default="NA", max_length=255, verbose_name=_("Translation Coding"))
    trans_estimate = models.CharField(default="NA", max_length=255, verbose_name=_("Translation Estimate"))
    trans_cost = models.CharField(default="NA", max_length=255, verbose_name=_("Translation Total Cost"))


class PubPublicationComResults(models.Model):
    Publication = models.ForeignKey(PubPublication, on_delete=models.DO_NOTHING, related_name="pub_com_results",
                                    verbose_name=_("Publication"))
    # publication = models.OneToOneField(PubPublication, on_delete=models.DO_NOTHING, primary_key=True)
    pub_category = models.ForeignKey(PccPublicationComResultsCategory, on_delete=models.DO_NOTHING, verbose_name=_("Category"))
    pub_description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    pub_size = models.CharField(default="NA", max_length=255, verbose_name=_("Size"))
    pub_attachment = models.CharField(default="NA", max_length=255, verbose_name=_("Attachment"))


class MepExpectedPublication(models.Model):
    meeting = models.ForeignKey(MetMeeting, on_delete=models.DO_NOTHING)
    publication = models.ForeignKey(PubPublication, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}".format(self.publication)


class PurOtherRegion(models.Model):
    pub_id = models.ForeignKey(PubPublication, on_delete=models.DO_NOTHING)
    # reg_id = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, blank=True, null=True)
    reg_id = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, blank=True, null=True)


class PuaOtherAuthor(models.Model):
    pub_id = models.ForeignKey(PubPublication, on_delete=models.DO_NOTHING)
    con_id = models.ForeignKey(ConContact, on_delete=models.DO_NOTHING)


class PukPublicationKeyword(models.Model):
    pub_id = models.ForeignKey(PubPublication, on_delete=models.DO_NOTHING)
    key_id = models.ForeignKey(KeyKeywords, on_delete=models.DO_NOTHING)


class PtiPublicationTitle(models.Model):
    pst_title = models.AutoField(primary_key=True)
    publication = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=100)
    language = models.ForeignKey(LanLanguage, on_delete=models.DO_NOTHING, null=True, blank=True)


# ----------------------------------------------------------------------------------------------------
# Create models for requests
#
class RepPriority(shared_models.Lookup):
    pass


class RetTiming(shared_models.Lookup):
    pass


class RedDecision(shared_models.Lookup):
    pass


class ResStatus(shared_models.Lookup):
    pass


class RdeDecisionExplanation(shared_models.Lookup):
    pass


class ReqRequest(models.Model):
    assigned_req_id = models.CharField(max_length=45, verbose_name=_("Assigned Request Number"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    in_year_request = models.BooleanField(verbose_name=_("In-Year Request"))
    # region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, blank=True, null=True)
    region = models.ForeignKey(shared_models.Region, on_delete=models.DO_NOTHING, blank=True, null=True,
                               verbose_name=_("Region"))
    client_sector = models.ForeignKey(SecSector, on_delete=models.DO_NOTHING, verbose_name=_("Client Sector"))
    client_name = models.CharField(max_length=100, verbose_name=_("Client Name"))
    client_title = models.CharField(max_length=100, verbose_name=_("Client Title"))
    client_email = models.CharField(max_length=255, verbose_name=_("Client E-mail"))
    issue = models.TextField(verbose_name=_("Issue"),
                             help_text=_("Issue requiring science information and/or advice. Posted as a question "
                                         "to be answered by Science."))
    priority = models.ForeignKey(RepPriority, on_delete=models.DO_NOTHING, verbose_name=_("Priority"))
    rationale = models.TextField(verbose_name=_("Rationale for Request"),
                                 help_text=_("Rationale or context for the request: What will the information/advice "
                                             "be used for? Who will be the end user(s)? Will it impact other DFO "
                                             "programs or regions?"))
    proposed_timing = models.ForeignKey(RetTiming, on_delete=models.DO_NOTHING, verbose_name=_("Proposed Timing"),
                                        help_text=_("Latest possible date to receive Science Advice."))
    rationale_for_timing = models.TextField(verbose_name=_("Rationale for Timing"),
                                            help_text=_("Explain rationale for proposed timing."))
    funding = models.BooleanField(help_text=_("Do you have funds to cover extra costs associated with this request?"))
    funding_notes = models.TextField(max_length=100, verbose_name=_("Funding Notes"))
    science_discussion = models.BooleanField(verbose_name=_("Science Discussion"),
                                             help_text=_("Have you talked to Science about this request?"))
    science_discussion_notes = models.CharField(max_length=100, verbose_name=_("Science Discussion Notes"),
                                                help_text=_("If you have talked to Science about this request, "
                                                            "to whom have you talked?"))
    # decision = models.ForeignKey(RedDecision, on_delete=models.DO_NOTHING, blank=True, null=True)
    # decision = models.ForeignKey(CotType, on_delete=models.DO_NOTHING)    # CotType is borrowed from Contacts
    # decision_explanation = models.TextField(max_length=100, verbose_name=_("Decision Explanation"))
    adviser_submission = models.DateField(null=True, blank=True, verbose_name=_("Client Adviser Submission Date"))
    rd_submission = models.DateField(null=True, blank=True, verbose_name=_("Client RD Submission Date"))
    decision_date = models.DateField(null=True, blank=True, verbose_name=_("Decision Date"))

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-id']


class ReqRequestCSAS(models.Model):
    request = models.OneToOneField(ReqRequest, on_delete=models.DO_NOTHING, primary_key=True)
    # status = models.ForeignKey(ResStatus, on_delete=models.DO_NOTHING, blank=True, null=True,
    #                            verbose_name=_("Status"))
    status = models.ForeignKey(ResStatus, on_delete=models.DO_NOTHING, verbose_name=_("Status"))
    trans_title = models.CharField(max_length=255, verbose_name=_("Translated Title"))
    decision = models.ForeignKey(RedDecision, on_delete=models.DO_NOTHING, blank=True, null=True,
                                 verbose_name=_("Decision"))
    decision_exp = models.ForeignKey(RdeDecisionExplanation, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     verbose_name=_("Decision Explanation"))
    decision_date = models.DateField(null=True, blank=True, verbose_name=_("Decision Date"))

    # def __str__(self):
    #     return "{}".format(self.request)

    # class Meta:
    #     ordering = ['-request']

# End of models.py
# ----------------------------------------------------------------------------------------------------
# 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
#
# class OthOther(models.Model):
#     oth_id = models.AutoField(primary_key=True)
#     oth_num = models.CharField(max_length=25)
#
#     def __str__(self):
#         return "{}".format(self.oth_num)
