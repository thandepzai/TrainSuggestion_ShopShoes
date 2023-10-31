from rest_framework import permissions


class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        disallowed_methods = ['POST', 'PUT', 'PATCH', 'DELETE']

        if request.method in disallowed_methods:
            return False
        return True
