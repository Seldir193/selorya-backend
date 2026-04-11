from django.conf import settings
from django.db import models
from apps.common.models import TimeStampedModel
from apps.listings.models import Listing


class Favorite(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "listing"],
                name="unique_user_listing_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.listing.title}"