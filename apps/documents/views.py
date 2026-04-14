from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Document
from .serializers import (
    DocumentCreateSerializer,
    DocumentSerializer,
    DocumentStatusUpdateSerializer,
)


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Document.objects.select_related("order", "recipient")
        if user.role == "admin" or user.is_superuser:
            return queryset
        return queryset.filter(recipient=user)


class DocumentCreateView(generics.CreateAPIView):
    serializer_class = DocumentCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        self.document = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = DocumentSerializer(
            self.document,
            context={"request": request},
        ).data
        return response


class DocumentStatusUpdateView(generics.UpdateAPIView):
    queryset = Document.objects.select_related("order", "recipient")
    serializer_class = DocumentStatusUpdateSerializer
    permission_classes = [IsAdminUser]