from rest_framework import serializers
from apps.categories.serializers import CategorySerializer
from .models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ListingImage
        fields = (
            "id",
            "image",
            "image_url",
            "alt_text",
            "sort_order",
            "is_primary",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("image_url",)

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return ""
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ListingSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.full_name", read_only=True)
    seller_email = serializers.CharField(source="seller.email", read_only=True)
    category_data = CategorySerializer(source="category", read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)

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
            "images",
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

    def validate_status(self, value):
        allowed = {"draft", "published", "sold", "archived"}
        if value not in allowed:
            raise serializers.ValidationError("Invalid listing status.")
        return value

    def create(self, validated_data):
        return Listing.objects.create(
            seller=self.context["request"].user,
            **validated_data,
        )


class ListingUpdateSerializer(serializers.ModelSerializer):
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

    def validate_status(self, value):
        allowed = {"draft", "published", "sold", "archived"}
        if value not in allowed:
            raise serializers.ValidationError("Invalid listing status.")
        return value


class ListingImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = (
            "image",
            "alt_text",
            "sort_order",
            "is_primary",
        )


class ListingImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = (
            "alt_text",
            "sort_order",
            "is_primary",
        )