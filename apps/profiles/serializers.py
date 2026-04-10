from rest_framework import serializers
from .models import CustomerProfile, SellerProfile


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = (
            "id",
            "phone",
            "city",
            "country",
            "created_at",
            "updated_at",
        )


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = (
            "id",
            "display_name",
            "bio",
            "city",
            "country",
            "created_at",
            "updated_at",
        )