from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Listing, ListingImage
from .permissions import IsSellerOrAdminOwner
from .serializers import (
    ListingCreateSerializer,
    ListingImageCreateSerializer,
    ListingImageSerializer,
    ListingImageUpdateSerializer,
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

        return queryset.select_related("seller", "category").prefetch_related("images")


class ListingDetailView(generics.RetrieveAPIView):
    queryset = Listing.objects.select_related(
        "seller",
        "category",
    ).prefetch_related("images")
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
        queryset = Listing.objects.select_related(
            "seller",
            "category",
        ).prefetch_related("images")
        if self.request.user.role == "admin" or self.request.user.is_superuser:
            return queryset
        return queryset.filter(seller=self.request.user)


class ListingUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Listing.objects.select_related(
        "seller",
        "category",
    ).prefetch_related("images")
    serializer_class = ListingUpdateSerializer
    permission_classes = [IsAuthenticated, IsSellerOrAdminOwner]
    lookup_field = "slug"


class ListingDeleteView(generics.DestroyAPIView):
    queryset = Listing.objects.select_related(
        "seller",
        "category",
    ).prefetch_related("images")
    permission_classes = [IsAuthenticated, IsSellerOrAdminOwner]
    lookup_field = "slug"


class ListingImageCreateView(generics.CreateAPIView):
    serializer_class = ListingImageCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, slug=self.kwargs["slug"])
        self.check_object_permissions(self.request, listing)
        if serializer.validated_data.get("is_primary"):
            ListingImage.objects.filter(listing=listing).update(is_primary=False)
        serializer.save(listing=listing)


class ListingImageListView(generics.ListAPIView):
    serializer_class = ListingImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        listing = get_object_or_404(Listing, slug=self.kwargs["slug"])
        if listing.status != "published":
            user = self.request.user
            allowed = user.is_authenticated and (
                user.role == "admin"
                or user.is_superuser
                or listing.seller_id == user.id
            )
            if not allowed:
                return ListingImage.objects.none()
        return ListingImage.objects.filter(listing=listing)


class ListingImageUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ListingImageUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ListingImage.objects.select_related("listing", "listing__seller")
        user = self.request.user
        if user.role == "admin" or user.is_superuser:
            return queryset
        return queryset.filter(listing__seller=user)

    def perform_update(self, serializer):
        image = self.get_object()
        if serializer.validated_data.get("is_primary"):
            ListingImage.objects.filter(
                listing=image.listing,
            ).exclude(id=image.id).update(is_primary=False)
        serializer.save()


class ListingImageDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ListingImage.objects.select_related("listing", "listing__seller")
        user = self.request.user
        if user.role == "admin" or user.is_superuser:
            return queryset
        return queryset.filter(listing__seller=user)