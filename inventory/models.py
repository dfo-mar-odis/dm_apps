from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
import os
import uuid
from django.utils.translation import gettext as _

from lib.functions.custom_functions import truncate, fiscal_year
from shared_models import models as shared_models
from dm_apps import custom_widgets

# Choices for language
ENG = 1
FRE = 2
LANGUAGE_CHOICES = (
    (ENG, 'English'),
    (FRE, 'French'),
)




class Location(models.Model):
    # Choices for surface_type
    CAN = 'Canada'
    US = 'United States'
    COUNTRY_CHOICES = (
        (CAN, 'Canada'),
        (US, 'United States'),
    )
    location_eng = models.CharField(max_length=1000, blank=True, null=True)
    location_fre = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES)
    abbrev_eng = models.CharField(max_length=25, blank=True, null=True)
    abbrev_fre = models.CharField(max_length=25, blank=True, null=True)
    uuid_gcmd = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.location_eng)


class Organization(models.Model):
    name_eng = models.CharField(max_length=1000, blank=True, null=True)
    name_fre = models.CharField(max_length=1000, blank=True, null=True)
    abbrev = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=7, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.name_eng, self.city) if self.city else "{}".format(self.name_eng)

    class Meta:
        ordering = ['name_eng']


class PersonRole(models.Model):
    role = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.role

    class Meta:
        ordering = ['id']


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="person")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    position_eng = models.CharField(max_length=255, blank=True, null=True)
    position_fre = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, blank=True, null=True, verbose_name=_("language preference"))
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.user.last_name, self.user.first_name)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def save(self, *args, **kwargs):
        self.full_name = "{} {}".format(self.user.first_name, self.user.last_name)

        super().save(*args, **kwargs)


class Status(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

        # return "{}  ({})".format(self.label, self.notes) if self.notes else "{}".format(self.label)


class SpatialRepresentationType(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label


class SpatialReferenceSystem(models.Model):
    label = models.CharField(max_length=255)
    code = models.CharField(max_length=25, blank=True, null=True)
    codespace = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label


class SecurityClassification(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.label


class ResourceType(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'inventory_resource_type'


class Maintenance(models.Model):
    frequency = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.frequency


class CharacterSet(models.Model):
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=25, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.label


class KeywordDomain(models.Model):
    name_eng = models.CharField(max_length=255, blank=True, null=True)
    name_fre = models.CharField(max_length=255, blank=True, null=True)
    abbrev = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    web_services = models.BooleanField()
    xml_block = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name_eng


class Keyword(models.Model):
    text_value_eng = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Keyword value (English)")
    text_value_fre = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Keyword value (French)")
    uid = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Unique Identifier")
    concept_scheme = models.CharField(max_length=1000, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    keyword_domain = models.ForeignKey(KeywordDomain, on_delete=models.DO_NOTHING, blank=True, null=True)
    xml_block = models.TextField(blank=True, null=True)
    is_taxonomic = models.BooleanField(default=False)

    def __str__(self):
        return self.text_value_eng

    class Meta:
        ordering = ["keyword_domain", "text_value_eng"]

    def save(self, *args, **kwargs):
        if self.keyword_domain.id == 2 or self.keyword_domain.id == 5:
            self.is_taxonomic = True
        super().save(*args, **kwargs)

    @property
    def non_hierarchical_name_en(self):
        # if the keyword can be split by " > " then take the last item in the list
        if len(self.text_value_eng.split(" > ")) > 1:
            return self.text_value_eng.split(" > ")[-1]
        else:
            return self.text_value_eng

    @property
    def non_hierarchical_name_fr(self):
        # if the keyword can be split by " > " then take the last item in the list
        if len(self.text_value_fre.split(" > ")) > 1:
            return self.text_value_fre.split(" > ")[-1]
        else:
            return self.text_value_fre


class Publication(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Citation(models.Model):
    title_eng = models.TextField(blank=True, null=True, verbose_name="Title (English)")
    title_fre = models.TextField(blank=True, null=True, verbose_name="Title (French)")
    authors = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.DO_NOTHING, blank=True, null=True)
    pub_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Publication Number")
    url_eng = models.TextField(blank=True, null=True, verbose_name="URL (English)")
    url_fre = models.TextField(blank=True, null=True, verbose_name="URL (French)")
    abstract_eng = models.TextField(blank=True, null=True, verbose_name="Abstract (English)")
    abstract_fre = models.TextField(blank=True, null=True, verbose_name="Abstract (French)")
    series = models.CharField(max_length=1000, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title_eng

    @property
    def short_citation(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        my_str = "{authors}. {year}. {title}. {publication} {pub_number}.".format(
            authors=self.authors,
            year=self.year,
            title=title,
            publication=self.publication,
            pub_number=self.pub_number,
        )

        return my_str

    @property
    def short_citation_html(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        if self.url_eng == None:
            my_str = "{authors}. {year}. {title}. {publication} {pub_number}.".format(
                authors=self.authors,
                year=self.year,
                title=title,
                publication=self.publication,
                pub_number=self.pub_number,
            )
        else:
            my_str = "{authors}. {year}. <a href=""{url_eng}""> {title}</a>. {publication} {pub_number}.".format(
                authors=self.authors,
                year=self.year,
                title=title,
                publication=self.publication,
                pub_number=self.pub_number,
                url_eng=self.url_eng,
            )
        return my_str

    @property
    def citation_br(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        my_str = "<b>Title:</b> {title}<br><b>Authors:</b> {authors}<br><b>Year:</b> {year}<br><b>Publication:</b> {publication}. {pub_number}".format(
            authors=self.authors,
            year=self.year,
            title=title,
            publication=self.publication,
            pub_number=self.pub_number,
        )
        return my_str

    @property
    def title(self):
        if self.title_eng != None:
            title = self.title_eng
        else:
            title = self.title_fre

        return title


class Resource(models.Model):
    # distribution_format choices
    from . import data_distribution_formats
    DISTRIBUTION_FORMAT_CHOICES = data_distribution_formats.DISTRIBUTION_FORMAT_CHOICES

    uuid = models.UUIDField(blank=True, null=True, verbose_name="UUID", unique=True)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.DO_NOTHING, blank=True, null=True)
    # section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="resources")
    section = models.ForeignKey(shared_models.Section, on_delete=models.DO_NOTHING, null=True, related_name="resources")
    title_eng = custom_widgets.OracleTextField(verbose_name="Title (English)")
    title_fre = custom_widgets.OracleTextField(blank=True, null=True, verbose_name="Title (French)")
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    maintenance = models.ForeignKey(Maintenance, on_delete=models.DO_NOTHING, blank=True, null=True,
                                    verbose_name="Maintenance frequency")
    purpose_eng = custom_widgets.OracleTextField(blank=True, null=True, verbose_name="Purpose (English)")
    purpose_fre = custom_widgets.OracleTextField(blank=True, null=True, verbose_name="Purpose (French)")
    descr_eng = custom_widgets.OracleTextField(blank=True, null=True, verbose_name="Description (English)")
    descr_fre = custom_widgets.OracleTextField(blank=True, null=True, verbose_name="Description (French)")
    time_start_day = models.IntegerField(blank=True, null=True, verbose_name="Start day")
    time_start_month = models.IntegerField(blank=True, null=True, verbose_name="Start month")
    time_start_year = models.IntegerField(blank=True, null=True, verbose_name="Start year")
    time_end_day = models.IntegerField(blank=True, null=True, verbose_name="End day")
    time_end_month = models.IntegerField(blank=True, null=True, verbose_name="End month")
    time_end_year = models.IntegerField(blank=True, null=True, verbose_name="End year")
    sampling_method_eng = models.TextField(blank=True, null=True, verbose_name="Sampling method (English)")
    sampling_method_fre = models.TextField(blank=True, null=True, verbose_name="Sampling method (French)")
    physical_sample_descr_eng = models.TextField(blank=True, null=True,
                                                 verbose_name="Description of physical samples (English)")
    physical_sample_descr_fre = models.TextField(blank=True, null=True,
                                                 verbose_name="Description of physical samples (French)")
    resource_constraint_eng = models.TextField(blank=True, null=True, verbose_name="Resource constraint (English)")
    resource_constraint_fre = models.TextField(blank=True, null=True, verbose_name="Resource constraint (French)")
    qc_process_descr_eng = models.TextField(blank=True, null=True, verbose_name="QC process description (English)")
    qc_process_descr_fre = models.TextField(blank=True, null=True, verbose_name="QC process description (French)")
    security_use_limitation_eng = models.CharField(max_length=255, blank=True, null=True,
                                                   verbose_name="Security use limitation (English)")
    security_use_limitation_fre = models.CharField(max_length=255, blank=True, null=True,
                                                   verbose_name="Security use limitation (French)")
    security_classification = models.ForeignKey(SecurityClassification, on_delete=models.DO_NOTHING, blank=True,
                                                null=True)
    storage_envr_notes = models.TextField(blank=True, null=True, verbose_name="Storage notes")
    distribution_format = models.CharField(max_length=255, blank=True, null=True, choices=DISTRIBUTION_FORMAT_CHOICES)
    data_char_set = models.ForeignKey(CharacterSet, on_delete=models.DO_NOTHING, blank=True, null=True,
                                      verbose_name="Data character set")
    spat_representation = models.ForeignKey(SpatialRepresentationType, on_delete=models.DO_NOTHING, blank=True,
                                            null=True, verbose_name="Spatial representation type")
    spat_ref_system = models.ForeignKey(SpatialReferenceSystem, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        verbose_name="Spatial reference system")
    geo_descr_eng = models.CharField(max_length=1000, blank=True, null=True,
                                     verbose_name="Geographic description (English)")
    geo_descr_fre = models.CharField(max_length=1000, blank=True, null=True,
                                     verbose_name="Geographic description (French)")
    west_bounding = models.FloatField(blank=True, null=True, verbose_name="West bounding coordinate")
    south_bounding = models.FloatField(blank=True, null=True, verbose_name="South bounding coordinate")
    east_bounding = models.FloatField(blank=True, null=True, verbose_name="East bounding coordinate")
    north_bounding = models.FloatField(blank=True, null=True, verbose_name="North bounding coordinate")
    parameters_collected_eng = models.TextField(blank=True, null=True, verbose_name="Parameters collected (English)")
    parameters_collected_fre = models.TextField(blank=True, null=True, verbose_name="Parameters collected (French)")
    additional_credit = models.TextField(blank=True, null=True)
    analytic_software = models.TextField(blank=True, null=True, verbose_name="Analytic software notes")
    date_verified = models.DateTimeField(blank=True, null=True)

    fgp_url = models.URLField(blank=True, null=True, verbose_name="Link to record on FGP")
    public_url = models.URLField(blank=True, null=True, verbose_name="Link to record on Open Gov't Portal")
    fgp_publication_date = models.DateTimeField(blank=True, null=True, verbose_name="Date published to FGP")
    od_publication_date = models.DateTimeField(blank=True, null=True, verbose_name="Date published to Open Gov't Portal")
    od_release_date = models.DateTimeField(blank=True, null=True, verbose_name="Date released to Open Gov't Portal")
    odi_id = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("ODIP Identifier"), unique=True)

    last_revision_date = models.DateTimeField(blank=True, null=True, verbose_name="Date of last published revision")
    open_data_notes = models.TextField(blank=True, null=True,
                                       verbose_name="Open data notes")
    notes = models.TextField(blank=True, null=True, verbose_name="General notes")
    citations = models.ManyToManyField(Citation, related_name='resources', blank=True)
    keywords = models.ManyToManyField(Keyword, related_name='resources', blank=True)
    people = models.ManyToManyField(Person, through='ResourcePerson')
    paa_items = models.ManyToManyField(shared_models.PAAItem, blank=True, verbose_name=_("Program Alignment Architecture (PAA) references"))
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, blank=True, null=True, related_name='children',
                               verbose_name="Parent resource")

    date_last_modified = models.DateTimeField(auto_now=True, editable=False)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    flagged_4_deletion = models.BooleanField(default=False)
    flagged_4_publication = models.BooleanField(default=False)
    completedness_report = models.TextField(blank=True, null=True, verbose_name=_("completedness report"))
    completedness_rating = models.FloatField(blank=True, null=True, verbose_name=_("completedness rating"))
    translation_needed = models.BooleanField(default=True, verbose_name=_("translation needed"))
    publication_fy = models.ForeignKey(shared_models.FiscalYear, on_delete=models.DO_NOTHING, blank=True, null=True, editable=False,
                                       verbose_name=_("FY of latest publication"))
    is_at_risk = models.BooleanField(default=False, verbose_name=_("Is your dataset at risk?"))


    def get_absolute_url(self):
        return reverse('inventory:resource_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return "({}) {}".format(self.id, getattr(self, str(_("title_eng"))))

    @property
    def t_title(self):
        return "{}".format(getattr(self, str(_("title_eng"))))

    @property
    def last_certification(self):
        return self.certification_history.fisrt()

    @property
    def last_publication(self):
        if self.fgp_publication_date:
            my_date = self.last_revision_date if self.last_revision_date else self.fgp_publication_date
            return my_date.strftime("%Y-%m-%d")

    def truncated_title(self):
        if self.title_eng:
            my_str = truncate(self.title_eng, 50)
        else:
            my_str = "no title"

        return my_str

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = uuid.uuid1()

        if self.fgp_publication_date:
            # if there is a revision date, use this, otherwise use fgp pub date
            pub_date = self.last_revision_date if self.last_revision_date else self.fgp_publication_date
            fy = shared_models.FiscalYear.objects.get(pk=fiscal_year(date=pub_date, sap_style=True))
            self.publication_fy = fy

        # will handle this through the resource form. If not, each time the record is verified, this field will be updated
        # self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    @property
    def thumbnail(self):
        for file in self.files.all():
            if "thumbnail" in file.caption.lower() or "vignette" in file.caption.lower():
                return file.file.url

    @property
    def bounds(self):
        if self.east_bounding and self.west_bounding and self.south_bounding and self.north_bounding:
            return [
                (self.east_bounding, self.north_bounding),
                (self.west_bounding, self.north_bounding),
                (self.west_bounding, self.south_bounding),
                (self.east_bounding, self.south_bounding),
            ]


class ContentType(models.Model):
    title = models.CharField(max_length=255, verbose_name="Name (English)")
    english_value = models.CharField(max_length=255, verbose_name="Name (French)")
    french_value = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.title)


class DataResource(models.Model):
    # choices for protocol
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    FTP = "FTP"
    PROTOCOL_CHOICES = [
        (HTTP, HTTP),
        (HTTPS, HTTPS),
        (FTP, FTP),
    ]
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="data_resources")
    url = models.URLField()
    name_eng = models.CharField(max_length=255, verbose_name="Name (English)")
    name_fre = models.CharField(max_length=255, verbose_name="Name (French)")
    protocol = models.CharField(max_length=255, choices=PROTOCOL_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.content_type, self.name_eng)


class WebService(models.Model):
    # choices for service_language
    ENG = "urn:xml:lang:eng-CAN"
    FRA = "urn:xml:lang:fra-CAN"
    SERVICE_LANGUAGE_CHOICES = [
        (ENG, "English"),
        (FRA, "French"),
    ]
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="web_services")
    protocol = models.CharField(max_length=255, default="ESRI REST: Map Service")
    service_language = models.CharField(max_length=255, choices=SERVICE_LANGUAGE_CHOICES)
    url = models.URLField()
    name_eng = models.CharField(max_length=255, verbose_name="Name (English)")
    name_fre = models.CharField(max_length=255, verbose_name="Name (French)")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.content_type, self.name_eng)


class ResourcePerson(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="resource_people")
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="resource_people")
    role = models.ForeignKey(PersonRole, on_delete=models.DO_NOTHING)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('resource', 'person', 'role'),)
        db_table = 'inventory_resource_people'
        ordering = ['role']

    def get_absolute_url(self):
        return reverse('inventory:resource_detail', kwargs={'pk': self.resource.id})


class BoundingBox(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    west_bounding = models.FloatField(blank=True, null=True)
    south_bounding = models.FloatField(blank=True, null=True)
    east_bounding = models.FloatField(blank=True, null=True)
    north_bounding = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class ResourceCertification(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, related_name="certification_history")
    certifying_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    certification_date = models.DateTimeField(blank=True, null=True, verbose_name="Date published to FGP")
    notes = models.TextField(blank=False, null=True)

    class Meta:
        ordering = ['-certification_date']
        db_table = 'inventory_resource_certification'


class Correspondence(models.Model):
    custodian = models.ForeignKey(User, on_delete=models.CASCADE, related_name="correspondences")
    subject = models.CharField(max_length=255)
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        ordering = ['-date']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     Person.profile.save()


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'inventory/resource_{0}/{1}'.format(instance.resource.id, filename)


class File(models.Model):
    caption = models.CharField(max_length=255)
    resource = models.ForeignKey(Resource, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
