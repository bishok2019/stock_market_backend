from django.db import models
from django.utils import timezone


class NotificationType(models.TextChoices):
    SYSTEM = "SYSTEM", "System Notification"
    NEW_USER = "NEW_USER", "New User"
    NEW_STOCK = "NEW_STOCK", "New Stock"


# Create your models here.
class Notification(models.Model):
    user = models.ManyToManyField(
        "authentication.CustomUser",
        through="UserNotification",
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=50, choices=NotificationType.choices, default=NotificationType.SYSTEM
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    # is_read = models.BooleanField(default=False)
    # read_at = models.DateTimeField(null=True, blank=True)
    stock = models.ForeignKey(
        "stock.Stock",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )

    # def mark_as_read(self):
    #     """Mark notification as read"""
    #     from django.utils import timezone

    #     self.is_read = True
    #     self.read_at = timezone.now()
    #     self.save()


# REMOVED: The mark_as_read method must be deleted or refactored
# as its logic now belongs entirely to the UserNotification model.
# If you want a similar method, it would need to accept a user argument
# and update the corresponding UserNotification object.


class UserNotification(models.Model):
    user = models.ForeignKey("authentication.CustomUser", on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "notification")
        # ordering = ["-notification__created_at"]

    def mark_as_read(self):
        """Mark notification as read"""

        self.is_read = True
        self.read_at = timezone.now()
        self.save()
