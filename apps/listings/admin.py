from django.contrib import admin
from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "seller",
        "category",
        "price",
        "condition",
        "status",
        "is_featured",
        "created_at",
    )
    list_filter = ("status", "condition", "is_featured", "category")
    search_fields = ("title", "slug", "seller__email", "seller__full_name")
    prepopulated_fields = {"slug": ("title",)}