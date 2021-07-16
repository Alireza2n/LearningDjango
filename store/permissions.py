from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user.is_anonymous:
            return False
        if obj.owner == request.user:
            return True
        return False


class IsOwnerOfParent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user.is_anonymous:
            return False
        if obj.order.owner == request.user:
            return True
        return False
