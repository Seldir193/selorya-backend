from datetime import date
from apps.orders.models import Order
from .models import Document


DOCUMENT_PREFIXES = {
    "invoice": "INV",
    "credit_note": "CRN",
    "cancellation": "CAN",
    "payment_reminder": "REM",
    "dunning_notice": "DUN",
}


def document_prefix(document_type: str) -> str:
    return DOCUMENT_PREFIXES[document_type]


def next_document_number(document_type: str) -> str:
    year = date.today().year
    prefix = document_prefix(document_type)
    count = Document.objects.filter(
        document_type=document_type,
        issue_date__year=year,
    ).count() + 1
    return f"{prefix}-{year}-{count:04d}"


def create_document(order: Order, document_type: str, notes: str = "") -> Document:
    recipient = order.buyer
    document = Document.objects.create(
        order=order,
        recipient=recipient,
        document_type=document_type,
        status="generated",
        document_number=next_document_number(document_type),
        issue_date=date.today(),
        notes=notes,
    )
    return document


def document_exists(order: Order, document_type: str) -> bool:
    return Document.objects.filter(
        order=order,
        document_type=document_type,
    ).exists()


def ensure_invoice(order: Order, notes: str = "") -> Document | None:
    if document_exists(order, "invoice"):
        return None
    return create_document(order, "invoice", notes)


def ensure_credit_note(order: Order, notes: str = "") -> Document | None:
    if document_exists(order, "credit_note"):
        return None
    return create_document(order, "credit_note", notes)


def ensure_cancellation(order: Order, notes: str = "") -> Document | None:
    if document_exists(order, "cancellation"):
        return None
    return create_document(order, "cancellation", notes)


def ensure_payment_reminder(order: Order, notes: str = "") -> Document | None:
    return create_document(order, "payment_reminder", notes)


def ensure_dunning_notice(order: Order, notes: str = "") -> Document | None:
    return create_document(order, "dunning_notice", notes)