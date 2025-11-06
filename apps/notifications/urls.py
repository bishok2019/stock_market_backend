from django.urls import include, path

from .views import (
    SystemNotificationListAPIView,
    SystemNotificationRetrieveAPIView,
)

notification_patterns = [
    path(
        "system-retrieve/<int:pk>",
        SystemNotificationRetrieveAPIView.as_view(),
        name="retrieve-notification",
    ),
    path(
        "system-list", SystemNotificationListAPIView.as_view(), name="list-notification"
    ),
]
urlpatterns = [
    path("notifications/", include(notification_patterns)),
]
