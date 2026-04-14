from django.utils import timezone
from rest_framework import serializers
from .models import Payment
from apps.orders.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id", read_only=True)
    buyer_email = serializers.CharField(source="order.buyer.email", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "order",
            "order_id",
            "buyer_email",
            "provider",
            "status",
            "amount",
            "currency",
            "external_reference",
            "paid_at",
            "created_at",
            "updated_at",
        )


class PaymentCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    provider = serializers.ChoiceField(choices=["stripe", "paypal", "manual"])
    external_reference = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        order = Order.objects.filter(id=attrs["order_id"]).first()
        if not order:
            raise serializers.ValidationError("Order not found.")
        if hasattr(order, "payment"):
            raise serializers.ValidationError("Payment already exists for this order.")
        attrs["order"] = order
        return attrs

    def create(self, validated_data):
        order = validated_data["order"]
        payment = Payment.objects.create(
            order=order,
            provider=validated_data["provider"],
            amount=order.total_amount,
            currency=order.currency,
            external_reference=validated_data.get("external_reference", ""),
        )
        return payment


class PaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("status", "external_reference")

    def update(self, instance, validated_data):
        status = validated_data.get("status", instance.status)
        instance.status = status
        instance.external_reference = validated_data.get(
            "external_reference",
            instance.external_reference,
        )
        if status == "paid" and not instance.paid_at:
            instance.paid_at = timezone.now()
            instance.order.status = "paid"
            instance.order.save(update_fields=["status", "updated_at"])
        if status in {"refunded", "partially_refunded"}:
            instance.order.status = "refunded"
            instance.order.save(update_fields=["status", "updated_at"])
        instance.save()
        return instance