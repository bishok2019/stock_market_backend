from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authentication.models import CustomUser
from apps.stock.models import Stock

from .services import NotificationService


@receiver(post_save, sender=Stock)
def create_new_stock_notification(sender, instance, created, **kwargs):
    """Create notifications when a new stock is added"""
    if created:
        NotificationService.notify_new_stock(instance)


@receiver(post_save, sender=CustomUser)
def creart_new_user_notification(sender, instance, created, **kwargs):
    if created:
        NotificationService.notify_new_user(instance)
