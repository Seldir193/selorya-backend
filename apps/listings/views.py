from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Listing
from .permissions import IsSellerOrAdminOwner
from .serializers import (
    ListingCreateSerializer,
    ListingSerializer,
    ListingUpdateSerializer,
)


class ListingListView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Listing.objects.filter(status="published")
        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(title__icontains=search)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.select_related("seller", "category")


class ListingDetailView(generics.RetrieveAPIView):
    queryset = Listing.objects.select_related("seller", "category")
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class ListingCreateView(generics.CreateAPIView):
    serializer_class = ListingCreateSerializer
    permission_classes = [IsAuthenticated]


class MyListingListView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Listing.objects.select_related("seller", "category")
        if self.request.user.role == "admin" or self.request.user.is_superuser:
            return queryset
        return queryset.filter(seller=self.request.user)


class ListingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Listing.objects.select_related("seller", "category")
    serializer_class = ListingUpdateSerializer
    permission_classes = [IsAuthenticated, IsSellerOrAdminOwner]
    lookup_field = "slug"


class ListingDeleteView(generics.DestroyAPIView):
    queryset = Listing.objects.select_related("seller", "category")
    permission_classes = [IsAuthenticated, IsSellerOrAdminOwner]
    lookup_field = "slug"