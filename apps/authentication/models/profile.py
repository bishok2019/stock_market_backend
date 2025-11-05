from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .custom_user import CustomUser


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Link to the user this profile belongs to.",
    )
    watchlisted_stock = models.ManyToManyField(
        "stock.Stock",
        blank=True,
        related_name="watchlisted_by_users",
        help_text="Stock watchlisted by user",
    )
    stock = models.ManyToManyField("stock.Stock", blank=True, related_name="stock")
