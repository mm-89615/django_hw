from rest_framework.permissions import BasePermission


class IsOwnerOrRead(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.creator == request.user
