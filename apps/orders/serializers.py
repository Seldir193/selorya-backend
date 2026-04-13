from rest_framework import serializers
from .models import Order, OrderItem
from apps.listings.models import Listing


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "listing",
            "seller",
            "title_snapshot",
            "price_snapshot",
            "quantity",
            "line_total",
            "created_at",
            "updated_at",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_email = serializers.CharField(source="buyer.email", read_only=True)
    buyer_name = serializers.CharField(source="buyer.full_name", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "buyer_email",
            "buyer_name",
            "status",
            "currency",
            "subtotal",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "buyer",
            "subtotal",
            "total_amount",
        )


class OrderCreateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        listing_id = attrs["listing_id"]
        quantity = attrs["quantity"]
        request = self.context["request"]
        listing = Listing.objects.select_related("seller").filter(
            id=listing_id,
            status="published",
        ).first()

        if not listing:
            raise serializers.ValidationError("Listing is not available.")
        if listing.seller_id == request.user.id:
            raise serializers.ValidationError("You cannot buy your own listing.")
        attrs["listing"] = listing
        attrs["quantity"] = quantity
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        listing = validated_data["listing"]
        quantity = validated_data["quantity"]

        order = Order.objects.create(buyer=request.user)
        OrderItem.objects.create(
            order=order,
            listing=listing,
            seller=listing.seller,
            title_snapshot=listing.title,
            price_snapshot=listing.price,
            quantity=quantity,
            line_total=listing.price * quantity,
        )
        order.recalculate_totals()
        return order