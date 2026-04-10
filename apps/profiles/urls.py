from django.urls import path
from .views import CustomerProfileMeView, SellerProfileMeView

urlpatterns = [
    path("customer/me/", CustomerProfileMeView.as_view(), name="customer-profile-me"),
    path("seller/me/", SellerProfileMeView.as_view(), name="seller-profile-me"),
]