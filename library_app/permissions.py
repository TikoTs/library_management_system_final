from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """
    Custom permission to only allow librarians to edit.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "librarian"
        )
