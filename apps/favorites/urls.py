from django.urls import path
from .views import FavoriteCreateView, FavoriteDeleteView, FavoriteListView

urlpatterns = [
    path("", FavoriteListView.as_view(), name="favorite-list"),
    path("create/", FavoriteCreateView.as_view(), name="favorite-create"),
    path("<int:pk>/delete/", FavoriteDeleteView.as_view(), name="favorite-delete"),
]