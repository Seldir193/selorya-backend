from rest_framework import serializers
from apps.categories.serializers import CategorySerializer
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.full_name", read_only=True)
    seller_email = serializers.CharField(source="seller.email", read_only=True)
    category_data = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Listing
        fields = (
            "id",
            "seller",
            "seller_name",
            "seller_email",
            "category",
            "category_data",
            "title",
            "slug",
            "description",
            "price",
            "condition",
            "status",
            "city",
            "country",
            "is_featured",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("seller",)


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = (
            "category",
            "title",
            "slug",
            "description",
            "price",
            "condition",
            "status",
            "city",
            "country",
            "is_featured",
        )

    def create(self, validated_data):
        return Listing.objects.create(
            seller=self.context["request"].user,
            **validated_data,
        )