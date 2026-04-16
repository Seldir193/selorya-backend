from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .checkout_services import (
    buyer_can_access_order,
    get_or_create_checkout_payment,
    mark_payment_paid,
)
from .models import Payment
from .paypal_service import capture_paypal_order, create_paypal_order
from .serializers import (
    CheckoutInitSerializer,
    PaymentCreateSerializer,
    PaymentSerializer,
    PaymentStatusUpdateSerializer,
)
from .services import sync_payment_status
from .stripe_service import construct_webhook_event, create_checkout_session


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


class StripeCheckoutCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]

        if not buyer_can_access_order(request.user, order):
            return Response(
                {"detail": "You cannot access this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        payment = get_or_create_checkout_payment(order, "stripe")
        session = create_checkout_session(order, payment)

        return Response(
            {
                "provider": "stripe",
                "payment_id": payment.id,
                "checkout_url": session.url,
                "session_id": session.id,
            },
            status=status.HTTP_200_OK,
        )


class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        signature = request.headers.get("Stripe-Signature", "")
        event = construct_webhook_event(request.body, signature)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            payment = Payment.objects.select_related("order").filter(
                external_reference=session["id"]
            ).first()
            if payment:
                mark_payment_paid(payment, session["id"])
                sync_payment_status(payment)

        return Response({"received": True}, status=status.HTTP_200_OK)


class PayPalOrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]

        if not buyer_can_access_order(request.user, order):
            return Response(
                {"detail": "You cannot access this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        payment = get_or_create_checkout_payment(order, "paypal")
        payload = create_paypal_order(order, payment)

        return Response(
            {
                "provider": "paypal",
                "payment_id": payment.id,
                "paypal_order_id": payload["paypal_order_id"],
                "approve_url": payload["approve_url"],
            },
            status=status.HTTP_200_OK,
        )


class PayPalCaptureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        payment = Payment.objects.select_related("order", "order__buyer").filter(
            pk=pk,
            provider="paypal",
        ).first()

        if not payment:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not buyer_can_access_order(request.user, payment.order):
            return Response(
                {"detail": "You cannot access this payment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        payload = capture_paypal_order(payment)
        if payload.get("status") == "COMPLETED":
            mark_payment_paid(payment, payment.external_reference)
            sync_payment_status(payment)

        return Response(
            {
                "payment": PaymentSerializer(payment).data,
                "paypal_capture": payload,
            },
            status=status.HTTP_200_OK,
        )