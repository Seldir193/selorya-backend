from django.urls import path
from .views import (
    ListingCreateView,
    ListingDeleteView,
    ListingDetailView,
    ListingListView,
    ListingUpdateView,
    MyListingListView,
)

urlpatterns = [
    path("", ListingListView.as_view(), name="listing-list"),
    path("create/", ListingCreateView.as_view(), name="listing-create"),
    path("mine/", MyListingListView.as_view(), name="my-listing-list"),
    path("<slug:slug>/", ListingDetailView.as_view(), name="listing-detail"),
    path(
        "<slug:slug>/update/",
        ListingUpdateView.as_view(),
        name="listing-update",
    ),
    path(
        "<slug:slug>/delete/",
        ListingDeleteView.as_view(),
        name="listing-delete",
    ),
]