from django.template.defaultfilters import yesno
from rest_framework import serializers

from lib.functions.custom_functions import listrify
from .. import models


class EntrySerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()
    regions = serializers.SerializerMethodField()
    sectors = serializers.SerializerMethodField()
    status = serializers.StringRelatedField()
    entry_type = serializers.StringRelatedField()
    date_created = serializers.SerializerMethodField()
    date_last_modified = serializers.SerializerMethodField()
    initial_date = serializers.SerializerMethodField()
    anticipated_end_date = serializers.SerializerMethodField()

    def get_regions(self, instance):
        return listrify(instance.regions.all())

    def get_organizations(self, instance):
        return listrify(instance.organizations.all())

    def get_sectors(self, instance):
        return listrify(instance.sectors.all())

    def get_date_created(self, instance):
        return instance.date_created.strftime("%Y-%m-%d") if instance.date_created else None

    def get_date_last_modified(self, instance):
        return instance.date_last_modified.strftime("%Y-%m-%d") if instance.date_last_modified else None

    def get_initial_date(self, instance):
        return instance.initial_date.strftime("%Y-%m-%d") if instance.initial_date else None

    def get_anticipated_end_date(self, instance):
        return instance.anticipated_end_date.strftime("%Y-%m-%d") if instance.anticipated_end_date else None

    funding_needed = serializers.SerializerMethodField()

    def get_funding_needed(self, instance):
        return yesno(instance.funding_needed, "yes,no,")

    class Meta:
        exclude = [
            "old_id",
            "last_modified_by",
            "created_by",
        ]
        model = models.Entry
