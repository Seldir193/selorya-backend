from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Payment
from .serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    PaymentStatusUpdateSerializer,
)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.select_related("order", "order__buyer")
        if user.role == "admin" or user.is_superuser:
            return queryset
        return queryset.filter(order__buyer=user)


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        self.payment = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = PaymentSerializer(self.payment).data
        return response


class PaymentStatusUpdateView(generics.UpdateAPIView):
    queryset = Payment.objects.select_related("order", "order__buyer")
    serializer_class = PaymentStatusUpdateSerializer
    permission_classes = [IsAdminUser]