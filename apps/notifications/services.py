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
        notification = Notification.objects.create(
            # user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            stock=stock,
        )
        # Then add users (handles both single user and list of users)
        if isinstance(user, list):
            notification.user.set(user)  # For multiple user
        else:
            notification.user.add(user)  # For Single User

        return notification

    # @staticmethod
    # def notify_new_stock(stock):
    #     """Create notifications for all users when a new stock is added"""
    #     notifications = []

    #     # for user in users:
    #     notification = Notification(
    #         notification_type=NotificationType.NEW_STOCK,
    #         title=f"New Stock Added: {stock.symbol}",
    #         message=f"A new stock {stock.name} ({stock.symbol}) has been added to the platform.",
    #         stock=stock,
    #     )
    #     notifications.append(notification)

    #     # Bulk create for better performance
    #     Notification.objects.bulk_create(notifications)

    #     return len(notifications)

    @staticmethod
    def notify_new_stock(stock):
        """Create notifications for all users when a new stock is added"""
        users = User.objects.filter(is_active=True)

        # Create single notification
        notification = Notification.objects.create(
            notification_type=NotificationType.NEW_STOCK,
            title=f"New Stock Added: {stock.symbol}",
            message=f"A new stock {stock.name} ({stock.symbol}) has been added to the platform.",
            stock=stock,
        )

        # Add all users to the notification
        notification.user.set(users)

        return users.count()

    @staticmethod
    def notify_new_user(user):
        """Send welcome notification to new users"""
        return NotificationService.create_notification(
            user=user,
            notification_type=NotificationType.NEW_USER,
            title="Welcome to Stock Market!",
            message=f"Welcome {user.username}!",
        )
