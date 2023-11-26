from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_staff and request.user.is_active:
            return False

        return True
