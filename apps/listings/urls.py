from django.urls import path
from .views import (
    ListingCreateView,
    ListingDeleteView,
    ListingDetailView,
    ListingImageCreateView,
    ListingImageDeleteView,
    ListingImageListView,
    ListingImageUpdateView,
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
    path(
        "<slug:slug>/images/",
        ListingImageListView.as_view(),
        name="listing-image-list",
    ),
    path(
        "<slug:slug>/images/create/",
        ListingImageCreateView.as_view(),
        name="listing-image-create",
    ),
    path(
        "images/<int:pk>/update/",
        ListingImageUpdateView.as_view(),
        name="listing-image-update",
    ),
    path(
        "images/<int:pk>/delete/",
        ListingImageDeleteView.as_view(),
        name="listing-image-delete",
    ),
]