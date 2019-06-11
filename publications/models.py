from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from shared_models import models as shared_models

import markdown


class Lookup(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Theme(Lookup):
    """
        Theme - Lookup table of Themes of which a publication can have multiple
    """
    pass


class Pillar(Lookup):
    """
        Pillar - Lookup table of Pillars of Sustainability of which a publication can have multiple
    """
    pass


class HumanComponent(Lookup):
    """
        HumanComponent - Lookup table of Human Components of which a publication can have multiple
    """
    pass


class EcosystemComponent(Lookup):
    """
        EcosystemComponent - Lookup table of Ecosystem Components of which a publication can have multiple
    """
    pass


class ProgramLinkage(Lookup):
    """
        ProgramLinkage - Lookup table of Program Linkage of which a
        publication can have multiple
    """
    pass


'''
TextLookup is intended to be used for many-to-one relationships where a DB table
has large non-searchable text blobs associated with a single project
'''


class TextLookup(models.Model):
    project = models.ForeignKey("Project", verbose_name=_("Project"), on_delete=models.CASCADE)
    value = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.value


class SpatialManagementDesignation(TextLookup):
    pass


class SpatialDataProduct(TextLookup):
    pass


class ComputerEnvironment(TextLookup):
    pass


class SourceDataInternal(TextLookup):
    pass


class SourceDataExternal(TextLookup):
    pass


class Publication(TextLookup):
    pass


class Site(TextLookup):
    pass


class Project(models.Model):
    # year
    # title
    # division <- region is a part of division
    # Linkage to national or regional program
    # Human component
    # Ecosystem component

    title = models.CharField(max_length=255, verbose_name=_("Project Title"))
    division = models.ForeignKey(shared_models.Division, on_delete=models.DO_NOTHING, blank=True, null=True,
                                 verbose_name=_("Division"))
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now,
                                              verbose_name=_("Date last modified"))

    abstract = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    # Todo: Last modified by isn't currently set in the new or update forms
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,
                                         related_name="pub_projects")

    theme = models.ManyToManyField(Theme, verbose_name=_("Theme(s)"))
    human_component = models.ManyToManyField(HumanComponent, verbose_name=_("Human Component(s)"))
    ecosystem_component = models.ManyToManyField(EcosystemComponent, verbose_name=_("Ecosystem Component(s)"))
    sustainability_pillar = models.ManyToManyField(Pillar, verbose_name=_("Pillar(s) of Sustainability"))
    program_linkage = models.ManyToManyField(ProgramLinkage, verbose_name=_("Program Linkage(s)"))

    class Meta:
        ordering = ['title', 'division']

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('publications:prj_detail', kwargs={'pk': self.pk})
