import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


def paypal_access_token():
    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
        auth=HTTPBasicAuth(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET,
        ),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def paypal_headers():
    token = paypal_access_token()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def create_paypal_order(order, payment):
    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders",
        headers=paypal_headers(),
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": str(order.id),
                    "custom_id": str(payment.id),
                    "amount": {
                        "currency_code": order.currency,
                        "value": str(order.total_amount),
                    },
                }
            ],
            "application_context": {
                "return_url": (
                    f"{settings.FRONTEND_URL}/checkout/success?provider=paypal"
                ),
                "cancel_url": (
                    f"{settings.FRONTEND_URL}/checkout/cancel?provider=paypal"
                ),
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    payment.external_reference = data["id"]
    payment.save(update_fields=["external_reference", "updated_at"])

    approve_url = ""
    for link in data.get("links", []):
        if link.get("rel") == "approve":
            approve_url = link.get("href", "")
            break

    return {
        "paypal_order_id": data["id"],
        "approve_url": approve_url,
        "raw": data,
    }


def capture_paypal_order(payment):
    response = requests.post(
        f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/"
        f"{payment.external_reference}/capture",
        headers=paypal_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()