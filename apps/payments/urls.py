from django.urls import path
from .views import PaymentCreateView, PaymentListView, PaymentStatusUpdateView

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("create/", PaymentCreateView.as_view(), name="payment-create"),
    path("<int:pk>/status/", PaymentStatusUpdateView.as_view(), name="payment-status"),
]