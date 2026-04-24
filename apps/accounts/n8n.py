import requests
from django.conf import settings


def registration_webhook_url() -> str:
    if not settings.N8N_WEBHOOK_BASE_URL:
        return ""
    return f"{settings.N8N_WEBHOOK_BASE_URL}{settings.N8N_REGISTRATION_WEBHOOK_PATH}"


def send_user_registered_to_n8n(user) -> None:
    url = registration_webhook_url()
    print("N8N webhook URL:", url)

    if not url:
        print("N8N webhook skipped: no URL configured")
        return

    payload = {
        "event": "user.registered",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "language": user.language,
        },
        "meta": {
            "source": "selorya-backend",
        },
    }

    print("N8N payload:", payload)

    try:
        response = requests.post(url, json=payload, timeout=10)
        print("N8N status:", response.status_code)
        print("N8N response:", response.text)
    except requests.RequestException as error:
        print("N8N webhook failed:", error)








