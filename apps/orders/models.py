from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.common.models import TimeStampedModel
from apps.listings.models import Listing


class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
        ("completed", "Completed"),
    ]

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    currency = models.CharField(max_length=10, default="EUR")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["-created_at"]

    def recalculate_totals(self):
        subtotal = sum(
            (item.line_total for item in self.items.all()),
            Decimal("0.00"),
        )
        self.subtotal = subtotal
        self.total_amount = subtotal
        self.save(update_fields=["subtotal", "total_amount", "updated_at"])

    def __str__(self):
        return f"Order<{self.id}> by {self.buyer.email}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sold_order_items",
    )
    title_snapshot = models.CharField(max_length=180)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        self.line_total = self.price_snapshot * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderItem<{self.order_id}:{self.title_snapshot}>"