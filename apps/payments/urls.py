from django.urls import path
from .views import (
    PaymentCreateView,
    PaymentListView,
    PaymentStatusUpdateView,
    PayPalCaptureView,
    PayPalOrderCreateView,
    StripeCheckoutCreateView,
    StripeWebhookView,
)

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("create/", PaymentCreateView.as_view(), name="payment-create"),
    path("<int:pk>/status/", PaymentStatusUpdateView.as_view(), name="payment-status"),
    path("stripe/checkout/", StripeCheckoutCreateView.as_view(), name="stripe-checkout"),
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("paypal/create-order/", PayPalOrderCreateView.as_view(), name="paypal-order"),
    path("paypal/<int:pk>/capture/", PayPalCaptureView.as_view(), name="paypal-capture"),
]