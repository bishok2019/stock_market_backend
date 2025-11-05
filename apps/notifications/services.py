from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.stock.models import Stock

from .models import Notification, NotificationType

User = get_user_model()


class NotificationService:
    """Service to handle notification creation and new stock and new user alert checking"""

    @staticmethod
    def create_notification(
        user,
        notification_type,
        title,
        message,
        stock=None,
    ):
        """Create a new notification"""
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            stock=stock,
        )

    @staticmethod
    def notify_new_stock(stock):
        """Create notifications for all users when a new stock is added"""
        users = User.objects.filter(is_active=True)
        notifications = []

        for user in users:
            notification = Notification(
                user=user,
                notification_type=NotificationType.NEW_STOCK,
                title=f"New Stock Added: {stock.symbol}",
                message=f"A new stock {stock.name} ({stock.symbol}) has been added to the platform.",
                stock=stock,
            )
            notifications.append(notification)

        # Bulk create for better performance
        Notification.objects.bulk_create(notifications)

        return len(notifications)
