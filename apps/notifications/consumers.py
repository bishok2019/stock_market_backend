import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Notification
from .serializers import UserNotificationListSerializer


class NotificationConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.user = self.scope["user"]

    #     # Check if user is authenticated
    #     if self.user.is_anonymous:
    #         await self.close()
    #         return

    #     # Create a unique group name for this user
    #     self.group_name = f"notifications_{self.user.id}"

    #     # Join notification group
    #     await self.channel_layer.group_add(self.group_name, self.channel_name)

    #     await self.accept()

    #     # Send existing notifications on connect
    #     notifications = await self.get_user_notifications()
    #     await self.send(
    #         text_data=json.dumps(
    #             {
    #                 "type": "initial_load",
    #                 "notifications": notifications,
    #                 "message": "Connected successfully",
    #             }
    #         )
    #     )

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
                    self.group_name = f"notifications_{user_id}"
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
                success = await self.mark_notification_read(notification_id)
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "mark_read_response",
                            "success": success,
                            "notification_id": notification_id,
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

    # @database_sync_to_async
    # def mark_notification_read(self, notification_id):
    #     try:
    #         notification = Notification.objects.get(id=notification_id, user=self.user)
    #         notification.mark_as_read()
    #         return True
    #     except Notification.DoesNotExist:
    #         return False
