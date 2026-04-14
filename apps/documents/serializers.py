from datetime import date
from rest_framework import serializers
from .models import Document
from apps.orders.models import Order


class DocumentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="order.id", read_only=True)
    recipient_email = serializers.CharField(source="recipient.email", read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            "id",
            "order",
            "order_id",
            "recipient",
            "recipient_email",
            "document_type",
            "status",
            "document_number",
            "issue_date",
            "file",
            "file_url",
            "notes",
            "created_at",
            "updated_at",
        )

    def get_file_url(self, obj):
        request = self.context.get("request")
        if not obj.file:
            return ""
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url


class DocumentCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    document_type = serializers.ChoiceField(
        choices=[
            "invoice",
            "credit_note",
            "cancellation",
            "payment_reminder",
            "dunning_notice",
        ]
    )
    document_number = serializers.CharField(max_length=80)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        order = Order.objects.select_related("buyer").filter(id=attrs["order_id"]).first()
        if not order:
            raise serializers.ValidationError("Order not found.")
        attrs["order"] = order
        return attrs

    def create(self, validated_data):
        order = validated_data["order"]
        return Document.objects.create(
            order=order,
            recipient=order.buyer,
            document_type=validated_data["document_type"],
            document_number=validated_data["document_number"],
            issue_date=date.today(),
            status="generated",
            notes=validated_data.get("notes", ""),
        )


class DocumentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("status", "notes")