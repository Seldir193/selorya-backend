from rest_framework.permissions import BasePermission


class IsSellerOrAdminOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == "admin" or user.is_superuser:
            return True
        return obj.seller_id == user.id