import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.authentication.models import CustomUser
from apps.stock.models import Stock

from .celery_tasks import send_new_stock_notification, send_new_user_notification
from .models import Notification
from .serializers import UserNotificationListSerializer
from .services import NotificationService

logger = logging.getLogger(__name__)
from django.db import transaction

# Synchronous
# @receiver(post_save, sender=Stock)
# def create_new_stock_notification(sender, instance, created, **kwargs):
#     """Create notifications when a new stock is added"""
#     if created:
#         NotificationService.notify_new_stock(instance)


# @receiver(post_save, sender=CustomUser)
# def creart_new_user_notification(sender, instance, created, **kwargs):
#     if created:
#         NotificationService.notify_new_user(instance)


# Asynchoronous
@receiver(post_save, sender=Stock)
def create_new_stock_notification(sender, instance, created, **kwargs):
    """Create notifications when a new stock is added"""
    if created:
        send_new_stock_notification.delay(instance.id)


@receiver(post_save, sender=CustomUser)
def creart_new_user_notification(sender, instance, created, **kwargs):
    if created:
        # print(instance.id)
        # print(instance.username)
        send_new_user_notification.delay(instance.id)


# Add signal for when notification is created to broadcast via WebSocket
##########Cannot use post_save for m-m relation
# @receiver(post_save, sender=Notification)
# def broadcast_notification(sender, instance, created, **kwargs):
#     """Broadcast notification to all associated users via WebSocket"""
#     if created:
#         channel_layer = get_channel_layer()
#         serializer = UserNotificationListSerializer(instance)

#         # Send to all users associated with this notification
#         for user in instance.user.all():
#             async_to_sync(channel_layer.group_send)(
#                 f"notifications_{user.id}",
#                 {"type": "notification_message", "notification": serializer.data},
#             )


@receiver(m2m_changed, sender=Notification.user.through)
def broadcast_notification(sender, instance, action, **kwargs):
    """Broadcast notification to all associated users via WebSocket"""
    # Only trigger when users are ADDED (not removed or cleared)
    if action == "post_add":
        logger.info(f"Broadcasting notification {instance.id} to user")

        channel_layer = get_channel_layer()
        serializer = UserNotificationListSerializer(instance)

        # Now instance.user.all() will actually have users!
        def _broadcast():
            for user in instance.user.all():
                group_name = (
                    f"notifications_for_{user.id}"  # group name must match to consumer
                )
                logger.info(f"Sending to {group_name}")

                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {"type": "notification_message", "notification": serializer.data},
                )

        # Enseure user receives notification only after all user related to notification is created.
        transaction.on_commit(_broadcast)
