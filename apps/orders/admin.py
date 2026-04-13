from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "listing",
        "seller",
        "title_snapshot",
        "price_snapshot",
        "quantity",
        "line_total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer",
        "status",
        "currency",
        "subtotal",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "currency")
    search_fields = ("buyer__email", "buyer__full_name")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "listing",
        "seller",
        "title_snapshot",
        "price_snapshot",
        "quantity",
        "line_total",
        "created_at",
    )
    search_fields = (
        "order__buyer__email",
        "seller__email",
        "title_snapshot",
        "listing__slug",
    )