import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.utils import A

from .filters import (ProjectFilter,)

from .models import (Analysis, Collection, Country, Data, MarineRegion,
                     Preservation, Project, Sample, SampleType, StorageType,
                     Subregion, Unit)


class CountryTable(tables.Table):
    country_name = tables.LinkColumn(
        'country_detail', args=[A('slug')], empty_values=())

    class Meta:
        model = Country
        template_name = "django_tables2/bootstrap.html"
        fields = ('country_name', 'country_code',)


class ProjectTable(tables.Table):
    name = tables.LinkColumn(
        'grainsize:project_detail', args=[
            A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ('name', 'pi', 'description')


class AnalysisTable(tables.Table):
    code = tables.LinkColumn('grainsize:analysis_detail', args=[
                             A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ('code', 'description',)


class CollectionTable(tables.Table):
    code = tables.LinkColumn('grainsize:collection_detail', args=[
                             A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ('code', 'description',)


class PreservationTable(tables.Table):
    code = tables.LinkColumn('grainsize:preservation_detail', args=[
                             A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ('code', 'description',)


class SampleTypeTable(tables.Table):
    code = tables.LinkColumn('grainsize:sampletype_detail', args=[
                             A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ('code', 'description',)


class StorageTypeTable(tables.Table):
    code = tables.LinkColumn('grainsize:storagetype_detail', args=[
                             A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = ('code', 'container', 'type',)


class SampleTable(tables.Table):
    event_number = tables.LinkColumn(
        'grainsize:sample_data', args=[
            A('pk')], empty_values=())

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'event_number',
            # 'project',
            'datetime',
            'latitude',
            'longitude',
            # 'analysis',
            # 'collection',
            # 'preservation',
            # 'storage',
            # 'start_depth',
            # 'end_depth',
            # 'sounding',
            'ancillary_data',
            # 'unit',
            'sample_id',
            'core',
            'filter',
            # 'filter_spm',
            'sample_type',
            'comment',
        )


class DataTable(tables.Table):
    diameter = tables.LinkColumn(
        'grainsize:data_detail', args=[
            A('pk')], empty_values=())

    class Meta:
        model = Sample
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('diameter', 'value',)
