from django.contrib import admin
from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("legal_name",)}


@admin.register(models.Individual)
class ContactAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name", "last_name")}

@admin.register(models.EngagementPlan)
class EngagementPlanAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(models.Interaction)
class InteractionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(models.InteractionObjective)
class InteractionObjectiveAdmin(admin.ModelAdmin):
    pass

@admin.register(models.InteractionSubject)
class InteractionSubjectAdmin(admin.ModelAdmin):
    pass