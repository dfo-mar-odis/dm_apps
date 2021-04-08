from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from shapely.geometry import Polygon, Point

from lib.functions.custom_functions import listrify, nz, fiscal_year
from shared_models import models as shared_models
from shared_models.models import SimpleLookup, UnilingualSimpleLookup, UnilingualLookup, FiscalYear, Region, MetadataFields
from shared_models.utils import format_coordinates


class FiltrationType(UnilingualLookup):
    pass


class DNAExtractionProtocol(UnilingualLookup):
    pass


class Tag(SimpleLookup):
    pass


class Species(models.Model):
    common_name_en = models.CharField(max_length=255, verbose_name=_("common name (EN)"))
    common_name_fr = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("common name (FR)"))
    scientific_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("scientific name"))
    tsn = models.IntegerField(blank=True, null=True, verbose_name="ITIS TSN")
    aphia_id = models.IntegerField(blank=True, null=True, verbose_name="AphiaID")

    @property
    def tcommon(self):
        # check to see if a french value is given
        if getattr(self, str(_("common_name_en"))):
            my_str = f'{getattr(self, str(_("common_name_en")))}'
        # if there is no translated term, just pull from the english field
        else:
            my_str = self.common_name_en
        return my_str

    def __str__(self):
        return self.tcommon

    class Meta:
        ordering = ['id']
        verbose_name_plural = _("Species")

    def get_absolute_url(self):
        return reverse('edna:species_detail', kwargs={'pk': self.id})

    @property
    def full_name(self):
        return "{} (<em>{}</em>)".format(self.common_name_en, self.scientific_name)

    @property
    def formatted_scientific(self):
        return f"<em>{self.scientific_name}</em>"


class Collection(UnilingualSimpleLookup, MetadataFields):
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, related_name='edna_collections', blank=True, null=True, verbose_name=_("DFO region"))
    program_description = models.TextField(blank=True, null=True, verbose_name=_("program description"))
    location_description = models.TextField(blank=True, null=True, verbose_name=_("area of operation"))
    province = models.ForeignKey(shared_models.Province, on_delete=models.DO_NOTHING, related_name='edna_collections', blank=True, null=True)
    contact_users = models.ManyToManyField(User, blank=True, verbose_name=_("contact DMApps user(s)"))
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("contact name"))
    contact_email = models.EmailField(max_length=255, blank=True, null=True, verbose_name=_("contact email"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("tags"))

    # calculated
    start_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=_("start date"))
    end_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=_("end date"))
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.DO_NOTHING, related_name="collections", blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        qs = self.samples.all()
        if qs.exists():
            self.start_date = qs.order_by("datetime").first().datetime
            self.end_date = qs.order_by("datetime").last().datetime
            self.fiscal_year_id = fiscal_year(self.end_date, sap_style=True)
        super().save(*args, **kwargs)

    @property
    def dates(self):
        my_str = date(self.start_date)
        if self.end_date:
            my_str += f" &rarr; {date(self.end_date)}"
        return mark_safe(my_str)

    @property
    def sample_count(self):
        return self.samples.count()

    @property
    def contacts(self):
        if self.contact_users.exists():
            return mark_safe(listrify([f'<a href="mailto:{u.email}">{u.get_full_name()}</a>' for u in self.contact_users.all()]))
        return mark_safe(f'<a href="mailto:{self.contact_email}">{self.contact_name}</a>')

    def get_absolute_url(self):
        return reverse("edna:collection_detail", args=[self.pk])

    def get_points(self):
        poly_points = list()
        for sample in self.samples.all():
            point = sample.get_point()
            if point:
                poly_points.append(point)
        return poly_points

    def get_polygon(self):
        points = self.get_points()
        if len(points) >= 3:
            return Polygon(points)

    def get_centroid(self):
        points = self.get_points()
        if self.get_polygon():
            p = self.get_polygon()
            return p.centroid
        elif len(points) > 0:
            return points[-1]


def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'edna/{0}/{1}'.format(instance.collection.id, filename)


class File(models.Model):
    collection = models.ForeignKey(Collection, related_name="files", on_delete=models.CASCADE, editable=False)
    caption = models.CharField(max_length=255)
    file = models.FileField(upload_to=file_directory_path)
    date_created = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption


class Sample(models.Model):
    collection = models.ForeignKey(Collection, related_name='samples', on_delete=models.DO_NOTHING, verbose_name=_("collection"), editable=False)
    unique_sample_identifier = models.CharField(max_length=255, unique=True, verbose_name=_("bottle unique identifier"))
    site_identifier = models.CharField(max_length=255, verbose_name=_("site identifier"), blank=True, null=True)
    site_description = models.TextField(verbose_name=_("site description"), blank=True, null=True)
    samplers = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("sampler(s)"))
    datetime = models.DateTimeField(verbose_name=_("collection date"), blank=False, null=True)
    latitude = models.FloatField(blank=False, null=True, verbose_name=_("latitude"))
    longitude = models.FloatField(blank=False, null=True, verbose_name=_("longitude"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("field comments"))

    class Meta:
        ordering = ["collection", "unique_sample_identifier"]

    def get_absolute_url(self):
        return reverse("edna:sample_detail", args=[self.pk])

    def __str__(self):
        return self.unique_sample_identifier

    def get_point(self):
        if self.latitude and self.longitude:
            return Point(self.latitude, self.longitude)

    @property
    def coordinates(self):
        my_str = "---"
        point = self.get_point()
        if point:
            my_str = format_coordinates(point.x, point.y, output_format="dd", sep="|")
        return mark_safe(my_str)


class Batch(models.Model):
    datetime = models.DateTimeField(default=timezone.now, verbose_name=_("start date/time"))
    operators = models.ManyToManyField(User, blank=True, verbose_name=_("operator(s)"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("comments"))

    class Meta:
        ordering = ["datetime"]
        abstract = True


class FiltrationBatch(Batch):
    class Meta:
        verbose_name_plural = _("Filtration Batches")

    def __str__(self):
        return "{} {} ({})".format(_("Filtration Batch"), self.id, self.datetime.strftime("%Y-%m-%d"))

    def get_absolute_url(self):
        return reverse('edna:filtration_batch_detail', kwargs={'pk': self.id})


class Filter(MetadataFields):
    """ the filter id of this table is effectively the tube id"""
    filtration_batch = models.ForeignKey(FiltrationBatch, related_name='filters', on_delete=models.DO_NOTHING, verbose_name=_("filtration batch"))
    sample = models.ForeignKey(Sample, related_name='filters', on_delete=models.DO_NOTHING, verbose_name=_("field sample"), blank=True, null=True)
    filtration_type = models.ForeignKey(FiltrationType, on_delete=models.DO_NOTHING, related_name="filters", verbose_name=_("filtration type"), default=1)
    start_datetime = models.DateTimeField(verbose_name=_("start time"))
    duration_min = models.IntegerField(verbose_name=_("duration (min)"), blank=True, null=True)
    filtration_volume_ml = models.FloatField(blank=True, null=True, verbose_name=_("volume (ml)"))
    storage_location = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("storage location"))
    comments = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("comments"))

    class Meta:
        ordering = ["filtration_batch", "sample"]


class ExtractionBatch(Batch):
    class Meta:
        verbose_name_plural = _("DNA Extraction Batches")

    def __str__(self):
        return "{} {} ({})".format(_("DNA Extraction Batch"), self.id, self.datetime.strftime("%Y-%m-%d"))

    def get_absolute_url(self):
        return reverse('edna:extraction_batch_detail', kwargs={'pk': self.id})


class DNAExtract(MetadataFields):
    """ the filter id of this table is effectively the tube id"""
    extraction_batch = models.ForeignKey(ExtractionBatch, related_name='extracts', on_delete=models.DO_NOTHING, verbose_name=_("extraction batch"))
    filter = models.OneToOneField(Filter, on_delete=models.CASCADE, blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name=_("start time"))
    dna_extraction_protocol = models.ForeignKey(DNAExtractionProtocol, on_delete=models.DO_NOTHING, verbose_name=_("extraction protocol"))
    storage_location = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("storage location"))
    comments = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("comments"))

    class Meta:
        ordering = ["extraction_batch", "filter_id"]


class PCRBatch(Batch):
    class Meta:
        verbose_name_plural = _("PCR Batches")

    def __str__(self):
        return "{} {} ({})".format(_("PCR Batch"), self.id, self.datetime.strftime("%Y-%m-%d"))

    def get_absolute_url(self):
        return reverse('edna:pcr_batch_detail', kwargs={'pk': self.id})


class PCR(MetadataFields):
    """ the filter id of this table is effectively the tube id"""
    pcr_batch = models.ForeignKey(PCRBatch, related_name='pcrs', on_delete=models.DO_NOTHING, verbose_name=_("PCR batch"))
    extract = models.ForeignKey(DNAExtract, on_delete=models.CASCADE, blank=True, null=True, related_name="pcrs", verbose_name=_("extract Id"))
    start_datetime = models.DateTimeField(verbose_name=_("start time"))
    pcr_number_prefix = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("PCR number prefix"))
    pcr_number_suffix = models.IntegerField(blank=True, null=True, verbose_name=_("PCR number suffix"))
    plate_id = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("plate Id"))
    position = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("position"))
    ipc_added = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("IPC added"))
    qpcr_ipc = models.FloatField(blank=True, null=True, verbose_name=_("qPCR IPC"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("comments"))

    class Meta:
        ordering = ["pcr_batch", "extract", "pcr_number_suffix"]

    def save(self, *args, **kwargs):
        # get the last PCR number suffix in the system
        super().save(*args, **kwargs)

    @property
    def pcr_number(self):
        return f'{nz(self.pcr_number_prefix, "")}:{nz(self.pcr_number_suffix, "")}'


class SpeciesObservation(MetadataFields):
    pcr = models.ForeignKey(PCR, related_name='observations', on_delete=models.DO_NOTHING, verbose_name=_("PCR"))
    species = models.ForeignKey(Species, related_name='observations', on_delete=models.DO_NOTHING, verbose_name=_("species"))
    ct = models.FloatField(blank=True, null=True, verbose_name=_("cycle threshold (ct)"))
    edna_conc = models.FloatField(blank=True, null=True, verbose_name=_("eDNA concentration (Pg/L)"))
    is_undetermined = models.BooleanField(default=False, verbose_name=_("undetermined?"))
    comments = models.TextField(null=True, blank=True, verbose_name=_("comments"))

    class Meta:
        ordering = ["pcr", "species"]
        unique_together = (("pcr", "species"),)
