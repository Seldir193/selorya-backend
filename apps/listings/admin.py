from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


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
    inlines = [ListingImageInline]


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = (
        "listing",
        "sort_order",
        "is_primary",
        "created_at",
    )
    list_filter = ("is_primary",)
    search_fields = ("listing__title", "listing__slug")