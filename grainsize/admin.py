from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import (Analysis, Collection, Country, Subregion, Data, MarineRegion,
                    Preservation, Project, Sample, SampleType,
                    StorageType, Unit)


# Register your models here.
@admin.register(Country)
class CountryAdmin(ImportExportActionModelAdmin):
    prepopulated_fields = {"slug": ("country_name",)}
    list_display = ('country_code', 'country_name')


@admin.register(Collection)
class CollectionAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Analysis)
class AnalysisAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Subregion)
class SubregionNameAdmin(ImportExportActionModelAdmin):
    list_display = ('subregion', 'code')


@admin.register(MarineRegion)
class MarineRegionAdmin(ImportExportActionModelAdmin):
    pass


# @admin.register(Method)
# class MethodAdmin(ImportExportActionModelAdmin):
#     pass


@admin.register(Preservation)
class PreservationAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Sample)
class SampleAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(SampleType)
class SampleTypeAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(StorageType)
class StorageTypeAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Data)
class SieveDataAdmin(ImportExportActionModelAdmin):
    pass
