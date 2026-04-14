from django.conf import settings
from django.db import models
from apps.common.models import TimeStampedModel
from apps.orders.models import Order


class Document(TimeStampedModel):
    TYPE_CHOICES = [
        ("invoice", "Invoice"),
        ("credit_note", "Credit note"),
        ("cancellation", "Cancellation"),
        ("payment_reminder", "Payment reminder"),
        ("dunning_notice", "Dunning notice"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("generated", "Generated"),
        ("sent", "Sent"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )
    document_number = models.CharField(max_length=80, unique=True)
    issue_date = models.DateField()
    file = models.FileField(upload_to="documents/", blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document_type}:{self.document_number}"