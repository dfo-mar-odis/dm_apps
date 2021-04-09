from rest_framework import permissions

from ..utils import has_grais_crud


class graisCRUDOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        elif has_grais_crud(request.user):
            return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        elif has_grais_crud(request.user):
            return True
