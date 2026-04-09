from django.conf import settings
from django.db import models
from apps.common.models import TimeStampedModel


class CustomerProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    phone = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, default="Germany")

    def __str__(self):
        return f"CustomerProfile<{self.user.email}>"


class SellerProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    display_name = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, default="Germany")

    def __str__(self):
        return f"SellerProfile<{self.user.email}>"