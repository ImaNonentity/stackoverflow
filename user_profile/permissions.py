from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
