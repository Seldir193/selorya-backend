from apps.documents.services import (
    ensure_cancellation,
    ensure_credit_note,
    ensure_invoice,
)
from .models import Payment


def sync_payment_status(payment: Payment) -> Payment:
    order = payment.order

    if payment.status == "paid":
        order.status = "paid"
        order.save(update_fields=["status", "updated_at"])
        ensure_invoice(order, "Invoice generated after payment.")
        return payment

    if payment.status in {"refunded", "partially_refunded"}:
        order.status = "refunded"
        order.save(update_fields=["status", "updated_at"])
        ensure_credit_note(order, "Credit note generated after refund.")
        return payment

    if payment.status == "cancelled":
        order.status = "cancelled"
        order.save(update_fields=["status", "updated_at"])
        ensure_cancellation(order, "Cancellation generated after payment cancel.")
        return payment

    return payment