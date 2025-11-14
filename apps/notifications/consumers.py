import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Notification
from .serializers import UserNotificationListSerializer

logger = logging.getLogger(__name__)


class PrivateNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user from scope (set by AuthMiddleware)
        self.user = self.scope.get("user")

        if self.user and self.user.is_authenticated:
            # Auto subscribes to user's own notification
            self.group_name = f"notifications_for_{self.user.id}"  # group name must match to signal where message being broadcast
            self.user_id = self.user.id
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            # Send initial notifications on connect
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "connection_success",
                        "message": "Connected successfully",
                    }
                )
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        "Handling incoming websocket messages"
        logger.info(f"Received: {text_data}")
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "mark_read":
                notification_id = data.get("notification_id")
                if not notification_id:
                    await self.send_error("notification_id is required")
                    return
                success = await self.mark_private_notification_as_read(notification_id)
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "mark_read_response",
                            "success": success,
                            "notification_id": (
                                "Notification marked as read"
                                if success
                                else "Failed to mark notification"
                            ),
                        }
                    )
                )
            ######################################################################
            elif action == "toggle_read_status":
                notification_id = data.get("notification_id")
                if not notification_id:
                    await self.send_error("notification id is required")
                    return
                else:
                    result = await self.toggle_notification_read_status(notification_id)

                if result:
                    is_read, success = result
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "toggle_read_response",
                                "success": success,
                                "notification_id": notification_id,
                                "is_read": is_read,
                                "message": (
                                    f"Notification marked as {'read' if is_read else 'unread'}"
                                    if success
                                    else "Failed to toggle notification"
                                ),
                            }
                        )
                    )
                else:
                    await self.send_error("Notification Not Found")

            ###########################################################################################

            elif action == "get_notifications":
                # Only get authenticated user's notifications
                notifications = await self.get_private_users_notification(self.user.id)
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "notification_list",
                            "notifications": notifications,
                            "message": "Notifications fetched successfully",
                        }
                    )
                )
            else:
                await self.send_error(f"Unknown action: {action}")

        except json.JSONDecodeError:
            await self.send_error("Invalid Json")
        except Exception as e:
            await self.send_error(str(e))

    async def send_error(self, message):
        "Helper method to send error messages"
        await self.send(text_data=json.dumps({"type": "error", "message": message}))

    # receives notifications from signals!
    async def notification_message(self, event):
        """Receive notification from group and send to WebSocket"""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_notification",
                    "notification": event["notification"],
                    "message": "New notification received",
                }
            )
        )

    @database_sync_to_async
    def get_private_users_notification(self, user_id):
        notification = Notification.objects.filter(user__id=user_id, is_read=False)
        serializer = UserNotificationListSerializer(notification, many=True)
        return serializer.data

    @database_sync_to_async
    def mark_private_notification_as_read(self, notification_id):
        try:
            notification = Notification.objects.filter(
                id=notification_id, user=self.user_id
            ).first()

            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False

    @database_sync_to_async
    def toggle_notification_read_status(self, notification_id):
        try:
            notification = Notification.objects.filter(
                id=notification_id, user=self.user_id
            ).first()

            if not notification:
                return None

            # Toggle the read status
            notification.is_read = not notification.is_read
            notification.save()

            return (notification.is_read, True)
        except Exception:
            return None


class NotificationConsumer(AsyncWebsocketConsumer):
    # Connect without Authorization
    async def connect(self):
        # Accept connection without authentication
        await self.accept()

        # Send connection success message
        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_success",
                    "message": "Connected successfully",
                }
            )
        )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "subscribe":
                # Subscribe to a user's notifications
                user_id = data.get("user_id")
                if user_id:
                    self.group_name = f"notifications_for_{user_id}"
                    self.user_id = user_id
                    await self.channel_layer.group_add(
                        self.group_name, self.channel_name
                    )

                    notifications = await self.get_user_notifications(user_id)
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "initial_load",
                                "notifications": notifications,
                                "message": "Subscribed successfully",
                            }
                        )
                    )
                else:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "error",
                                "message": "user_id is required",
                            }
                        )
                    )
            elif action == "mark_read":
                notification_id = data.get("notification_id")
                user_id = data.get("user_id")

                if not notification_id or not user_id:
                    await self.send_error("notification_id and user_id are required")
                    return

                success = await self.mark_notification_read(notification_id, user_id)
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "mark_read_response",
                            "success": success,
                            "notification_id": notification_id,
                            "message": "Notification Marked as Read.",
                        }
                    )
                )
            elif action == "get_notifications":
                user_id = data.get("user_id", getattr(self, "user_id", None))
                if user_id:
                    notifications = await self.get_user_notifications(user_id)
                    await self.send(
                        text_data=json.dumps(
                            {
                                "type": "notification_list",
                                "notifications": notifications,
                                "message": "Notification fetched Successfully.",
                            }
                        )
                    )
        except Exception as e:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": str(e),
                    }
                )
            )

    async def notification_message(self, event):
        """Receive notification from group and send to WebSocket"""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_notification",
                    "notification": event["notification"],
                    "message": "New notification received",
                }
            )
        )

    @database_sync_to_async
    def get_user_notifications(self, user_id):
        notifications = Notification.objects.filter(user__id=user_id).order_by("-id")[
            :50
        ]
        serializer = UserNotificationListSerializer(notifications, many=True)
        return serializer.data

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id, user_id):
        try:
            notification = Notification.objects.get(
                id=notification_id, user__id=user_id
            )
            notification.mark_as_read(notification_id, user_id)
            return True
        except Notification.DoesNotExist:
            return False
