from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanSeePublic(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            raise PermissionDenied("У вас недостаточно прав")
