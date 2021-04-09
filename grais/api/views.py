from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_models.utils import get_labels
from . import serializers
from .permissions import graisCRUDOrReadOnly
from .. import models


# USER
#######
class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserDisplaySerializer(instance=request.user)
        data = serializer.data
        return Response(data)


class SampleSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SampleSpeciesSerializer
    permission_classes = [graisCRUDOrReadOnly]
    queryset = models.SampleSpecies.objects.all()

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("sample"):
            sample = get_object_or_404(models.Sample, pk=qp.get("sample"))
            qs = sample.sample_spp.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a sample"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



class LineSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LineSpeciesSerializer
    permission_classes = [graisCRUDOrReadOnly]
    queryset = models.LineSpecies.objects.all()

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("line"):
            line = get_object_or_404(models.Line, pk=qp.get("line"))
            qs = line.line_spp.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a line"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



class SurfaceSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SurfaceSpeciesSerializer
    permission_classes = [graisCRUDOrReadOnly]
    queryset = models.SurfaceSpecies.objects.all()

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("surface"):
            surface = get_object_or_404(models.Surface, pk=qp.get("surface"))
            qs = surface.surface_spp.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a surface"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



class SpeciesModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Species

    def get(self, request):
        data = dict()
        data['labels'] = get_labels(self.model)
        data['choices'] = [dict(text=item.choice_display, value=item.id) for item in self.model.objects.all()]
        return Response(data)

#
# class DNAExtractViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.DNAExtractSerializer
#     permission_classes = [eDNACRUDOrReadOnly]
#     queryset = models.DNAExtract.objects.all()
#
#     # pagination_class = StandardResultsSetPagination
#
#     def list(self, request, *args, **kwargs):
#         qp = request.query_params
#         if qp.get("batch"):
#             batch = get_object_or_404(models.ExtractionBatch, pk=qp.get("batch"))
#             qs = batch.extracts.all()
#             serializer = self.get_serializer(qs, many=True)
#             return Response(serializer.data)
#         raise ValidationError(_("You need to specify a batch"))
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user, updated_by=self.request.user)
#
#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)
#
#
# class DNAExtractModelMetaAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     model = models.DNAExtract
#
#     def get(self, request):
#         data = dict()
#         data['labels'] = get_labels(self.model)
#         # we want to get a list of filters for which there has been no PCRs
#         data['filter_choices'] = [dict(text=item.id, value=item.id, has_extract=hasattr(item, 'extract')) for item in models.Filter.objects.all()]
#         data['dna_extraction_protocol_choices'] = [dict(text=item.name, value=item.id) for item in models.DNAExtractionProtocol.objects.all()]
#
#         return Response(data)
#
#
# class PCRViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.PCRSerializer
#     permission_classes = [eDNACRUDOrReadOnly]
#     queryset = models.PCR.objects.all()
#
#     # pagination_class = StandardResultsSetPagination
#
#     def list(self, request, *args, **kwargs):
#         qp = request.query_params
#         if qp.get("batch"):
#             batch = get_object_or_404(models.PCRBatch, pk=qp.get("batch"))
#             qs = batch.pcrs.all()
#             serializer = self.get_serializer(qs, many=True)
#             return Response(serializer.data)
#         raise ValidationError(_("You need to specify a batch"))
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user, updated_by=self.request.user)
#
#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)
#
#
# class PCRModelMetaAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     model = models.PCR
#
#     def get(self, request):
#         data = dict()
#         data['labels'] = get_labels(self.model)
#         # we want to get a list of filters for which there has been no PCRs
#         data['extract_choices'] = [dict(text=item.id, value=item.id, has_pcr=item.pcrs.exists()) for item in models.DNAExtract.objects.all()]
#
#         qs = models.PCR.objects.filter(pcr_number_suffix__isnull=False).order_by("pcr_number_suffix")
#         last_pcr_number = 0
#         if qs.exists():
#             last_pcr_number = qs.last().pcr_number_suffix
#         data['last_pcr_number'] = last_pcr_number
#
#         return Response(data)
#
#
# class SpeciesObservationViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.SpeciesObservationSerializer
#     permission_classes = [eDNACRUDOrReadOnly]
#     queryset = models.SpeciesObservation.objects.all()
#
#     # pagination_class = StandardResultsSetPagination
#
#     def list(self, request, *args, **kwargs):
#         qp = request.query_params
#         if qp.get("pcr"):
#             pcr = get_object_or_404(models.PCR, pk=qp.get("pcr"))
#             qs = pcr.observations.all()
#             serializer = self.get_serializer(qs, many=True)
#             return Response(serializer.data)
#         raise ValidationError(_("You need to specify a PCR"))
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user, updated_by=self.request.user)
#
#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)
#
#
# class SpeciesObservationModelMetaAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     model = models.SpeciesObservation
#
#     def get(self, request):
#         data = dict()
#         data['labels'] = get_labels(self.model)
#         # we want to get a list of filters for which there has been no SpeciesObservations
#         data['species_choices'] = [dict(text=str(item), value=item.id) for item in models.Species.objects.all()]
#         return Response(data)
