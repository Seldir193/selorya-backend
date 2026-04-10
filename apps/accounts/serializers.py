from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.profiles.serializers import (
    CustomerProfileSerializer,
    SellerProfileSerializer,
)
from .models import User


class UserSerializer(serializers.ModelSerializer):
    customer_profile = CustomerProfileSerializer(read_only=True)
    seller_profile = SellerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "role",
            "language",
            "is_email_verified",
            "created_at",
            "updated_at",
            "customer_profile",
            "seller_profile",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "full_name", "role", "language", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=request, username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        attrs["user"] = user
        return attrs