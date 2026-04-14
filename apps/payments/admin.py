from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "provider",
        "status",
        "amount",
        "currency",
        "paid_at",
        "created_at",
    )
    list_filter = ("provider", "status", "currency")
    search_fields = (
        "order__buyer__email",
        "external_reference",
    )