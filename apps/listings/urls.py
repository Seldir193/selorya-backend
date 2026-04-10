from django.urls import path
from .views import (
    ListingCreateView,
    ListingDetailView,
    ListingListView,
    MyListingListView,
)

urlpatterns = [
    path("", ListingListView.as_view(), name="listing-list"),
    path("create/", ListingCreateView.as_view(), name="listing-create"),
    path("mine/", MyListingListView.as_view(), name="my-listing-list"),
    path("<slug:slug>/", ListingDetailView.as_view(), name="listing-detail"),
]