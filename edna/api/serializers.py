from django.contrib.auth.models import User
from rest_framework import serializers

from .. import models


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", ]


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Filter
        fields = "__all__"


class DNAExtractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DNAExtract
        fields = "__all__"


class SpeciesObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpeciesObservation
        fields = "__all__"

    species_display = serializers.SerializerMethodField()

    def get_species_display(self, instance):
        return str(instance.species)


class PCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PCR
        fields = "__all__"

    pcr_number = serializers.SerializerMethodField()
    observations = SpeciesObservationSerializer(many=True, read_only=True)

    def get_pcr_number(self, instance):
        return instance.pcr_number
