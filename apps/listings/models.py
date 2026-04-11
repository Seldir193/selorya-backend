from django.conf import settings
from django.db import models
from apps.categories.models import Category
from apps.common.models import TimeStampedModel


class Listing(TimeStampedModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("sold", "Sold"),
        ("archived", "Archived"),
    ]

    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like new"),
        ("very_good", "Very good"),
        ("good", "Good"),
        ("acceptable", "Acceptable"),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="listings",
    )
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="good",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, default="Germany")
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ListingImage(TimeStampedModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="listings/")
    alt_text = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return f"Image<{self.listing_id}>"