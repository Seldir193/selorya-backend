from django.utils import timezone
from .models import Payment
from apps.orders.models import Order


def buyer_can_access_order(user, order: Order) -> bool:
    if user.role == "admin" or user.is_superuser:
        return True
    return order.buyer_id == user.id


def get_or_create_checkout_payment(order: Order, provider: str) -> Payment:
    payment = getattr(order, "payment", None)
    if payment:
        payment.provider = provider
        payment.amount = order.total_amount
        payment.currency = order.currency
        payment.status = "pending"
        payment.paid_at = None
        payment.save(
            update_fields=[
                "provider",
                "amount",
                "currency",
                "status",
                "paid_at",
                "updated_at",
            ]
        )
        return payment

    return Payment.objects.create(
        order=order,
        provider=provider,
        amount=order.total_amount,
        currency=order.currency,
        status="pending",
    )


def mark_payment_paid(payment: Payment, external_reference: str = "") -> Payment:
    payment.status = "paid"
    payment.external_reference = external_reference or payment.external_reference
    if not payment.paid_at:
        payment.paid_at = timezone.now()
    payment.save()
    return payment


def mark_payment_cancelled(payment: Payment, external_reference: str = "") -> Payment:
    payment.status = "cancelled"
    payment.external_reference = external_reference or payment.external_reference
    payment.save()
    return payment