from django.contrib import admin
from .models import CustomerProfile, SellerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "country", "created_at")
    search_fields = ("user__email", "user__full_name", "city")


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "city", "country", "created_at")
    search_fields = ("user__email", "user__full_name", "display_name")