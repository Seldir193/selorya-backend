from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "role",
        "language",
        "is_email_verified",
        "is_active",
        "created_at",
    )
    list_filter = ("role", "language", "is_active", "is_email_verified")
    search_fields = ("email", "full_name")