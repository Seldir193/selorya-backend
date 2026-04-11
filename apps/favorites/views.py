from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .serializers import FavoriteCreateSerializer, FavoriteSerializer


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user,
        ).select_related(
            "listing",
            "listing__seller",
            "listing__category",
        )


class FavoriteCreateView(generics.CreateAPIView):
    serializer_class = FavoriteCreateSerializer
    permission_classes = [IsAuthenticated]


class FavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)