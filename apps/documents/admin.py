from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "document_number",
        "document_type",
        "status",
        "order",
        "recipient",
        "issue_date",
        "created_at",
    )
    list_filter = ("document_type", "status", "issue_date")
    search_fields = (
        "document_number",
        "order__buyer__email",
        "recipient__email",
    )