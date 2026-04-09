from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .models import CustomerProfile, SellerProfile


@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if not created:
        return
    CustomerProfile.objects.create(user=instance)
    SellerProfile.objects.create(
        user=instance,
        display_name=instance.full_name,
    )