from django.contrib.auth.models import User
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_models.utils import special_capitalize
from . import serializers
# USER
#######
from .pagination import StandardResultsSetPagination


def _get_labels(model):
    labels = {}
    for field in model._meta.get_fields():
        if hasattr(field, "name") and hasattr(field, "verbose_name"):
            labels[field.name] = special_capitalize(field.verbose_name)
    return labels


class UserListAPIView(ListAPIView):
    queryset = User.objects.order_by("first_name", "last_name")
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'id']


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.CurrentUserSerializer(instance=request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
