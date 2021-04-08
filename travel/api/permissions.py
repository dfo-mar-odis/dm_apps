from rest_framework import permissions

#
# class IsSuperuser(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_superuser
#
#
# class IsOceanUser(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.profile.oceanography
#
from travel.models import Trip
from travel.utils import can_modify_request, is_admin, in_adm_admin_group


# from ..utils import can_modify_project


class CanModifyOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.id:
            return True
        if hasattr(obj, "request_id"):
            return can_modify_request(request.user, obj.request_id)
        elif hasattr(obj, "traveller"):
            return can_modify_request(request.user, obj.traveller.request_id)
        else:
            return can_modify_request(request.user, obj.id)


class TravelAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.id:
            return True
        else:
            if isinstance(obj, Trip) and not obj.is_adm_approval_required:
                return is_admin(request.user)
            else:
                return in_adm_admin_group(request.user)
