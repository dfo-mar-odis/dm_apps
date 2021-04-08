from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework_csv.renderers import CSVRenderer

from . import serializers
from .. import models


class EntryCSVAPIView(ListAPIView):
    renderer_classes = [CSVRenderer]
    serializer_class = serializers.EntrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Entry.objects.all()
