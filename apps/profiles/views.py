from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomerProfile, SellerProfile
from .serializers import CustomerProfileSerializer, SellerProfileSerializer


class CustomerProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CustomerProfile.objects.get(user=self.request.user)


class SellerProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return SellerProfile.objects.get(user=self.request.user)