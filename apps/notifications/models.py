from django.db import models


class NotificationType(models.TextChoices):
    SYSTEM = "SYSTEM", "System Notification"
    NEW_USER = "NEW_USER", "New User"
    NEW_STOCK = "NEW_STOCK", "New Stock"


# Create your models here.
class Notification(models.Model):
    user = models.ManyToManyField(
        "authentication.CustomUser",
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=50, choices=NotificationType.choices, default=NotificationType.SYSTEM
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    stock = models.ForeignKey(
        "stock.Stock",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )

    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone

        self.is_read = True
        self.read_at = timezone.now()
        self.save()
