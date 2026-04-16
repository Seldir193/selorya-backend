from django.urls import path
from .views import (
    DocumentCreateView,
    DocumentListView,
    DocumentSendView,
    DocumentStatusUpdateView,
)

urlpatterns = [
    path("", DocumentListView.as_view(), name="document-list"),
    path("create/", DocumentCreateView.as_view(), name="document-create"),
    path("<int:pk>/status/", DocumentStatusUpdateView.as_view(), name="document-status"),
    path("<int:pk>/send/", DocumentSendView.as_view(), name="document-send"),
]