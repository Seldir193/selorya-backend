import stripe
from django.conf import settings


def stripe_client():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def create_checkout_session(order, payment):
    client = stripe_client()
    session = client.checkout.Session.create(
        mode="payment",
        success_url=(
            f"{settings.FRONTEND_URL}/checkout/success"
            f"?provider=stripe&session_id={{CHECKOUT_SESSION_ID}}"
        ),
        cancel_url=f"{settings.FRONTEND_URL}/checkout/cancel?provider=stripe",
        client_reference_id=str(order.id),
        metadata={
            "order_id": str(order.id),
            "payment_id": str(payment.id),
        },
        line_items=[
            {
                "quantity": item.quantity,
                "price_data": {
                    "currency": order.currency.lower(),
                    "unit_amount": int(item.price_snapshot * 100),
                    "product_data": {
                        "name": item.title_snapshot,
                    },
                },
            }
            for item in order.items.all()
        ],
    )
    payment.external_reference = session.id
    payment.save(update_fields=["external_reference", "updated_at"])
    return session


def construct_webhook_event(payload, signature_header):
    client = stripe_client()
    return client.Webhook.construct_event(
        payload=payload,
        sig_header=signature_header,
        secret=settings.STRIPE_WEBHOOK_SECRET,
    )