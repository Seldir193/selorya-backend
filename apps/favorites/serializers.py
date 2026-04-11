from rest_framework import serializers
from .models import Favorite


class FavoriteListingSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="listing.id")
    slug = serializers.CharField(source="listing.slug")
    title = serializers.CharField(source="listing.title")
    price = serializers.DecimalField(
        source="listing.price",
        max_digits=10,
        decimal_places=2,
    )
    status = serializers.CharField(source="listing.status")
    city = serializers.CharField(source="listing.city")
    country = serializers.CharField(source="listing.country")
    seller_name = serializers.CharField(source="listing.seller.full_name")
    category_name = serializers.CharField(source="listing.category.name")


class FavoriteSerializer(serializers.ModelSerializer):
    listing_data = FavoriteListingSerializer(source="*", read_only=True)

    class Meta:
        model = Favorite
        fields = (
            "id",
            "listing",
            "listing_data",
            "created_at",
            "updated_at",
        )


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("listing",)

    def validate(self, attrs):
        user = self.context["request"].user
        listing = attrs["listing"]
        exists = Favorite.objects.filter(user=user, listing=listing).exists()
        if exists:
            raise serializers.ValidationError("Listing is already favorited.")
        return attrs

    def create(self, validated_data):
        return Favorite.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )