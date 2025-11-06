from celery import shared_task
from django.contrib.auth import get_user_model

from .models import NotificationType
from .services import NotificationService

User = get_user_model()


@shared_task(bind=True, max_retries=3)
def send_new_stock_notification(self, stock_id):
    """Asynchronously notify all users about new stock"""
    try:
        from apps.stock.models import Stock

        stock = Stock.objects.get(id=stock_id)
        count = NotificationService.notify_new_stock(stock)
        return f"Sent notification to {count} users"
    except Stock.DoesNotExist:
        return f"Stock {stock_id} not found"
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2**self.request.retries))


@shared_task
def send_new_user_notification(user_id):
    """Send welcome notification to new user"""
    try:
        user = User.objects.get(id=user_id)
        NotificationService.notify_new_user(user)
        return f"Welcome notification sent to {user.username}"
    except User.DoesNotExist:
        return f"User {user_id} not found"


@shared_task
def mark_notification_as_read(notification_id):
    """Mark notification as read asynchronously"""
    from .models import Notification

    try:
        notification = Notification.objects.get(id=notification_id)
        notification.mark_as_read()
        return f"Notification {notification_id} marked as read"
    except Notification.DoesNotExist:
        return f"Notification {notification_id} not found"
