from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from apps.common.models import TimeStampedModel
from .managers import UserManager


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("seller", "Seller"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=160)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    language = models.CharField(max_length=10, default="de")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email











# from django.contrib.auth.base_user import BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.full_clean()
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("role", "admin")
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(email, password, **extra_fields)