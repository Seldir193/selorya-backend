from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Listing
from .serializers import ListingCreateSerializer, ListingSerializer


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
        return Listing.objects.filter(
            seller=self.request.user,
        ).select_related("seller", "category")