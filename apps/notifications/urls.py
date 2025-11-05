from django.urls import include, path

from .views import NotificationListAPIView, NotificationRetrieveAPIView

notification_patterns = [
    path(
        "retrieve/<int:pk>",
        NotificationRetrieveAPIView.as_view(),
        name="retrieve-notification",
    ),
    path("list", NotificationListAPIView.as_view(), name="list-notification"),
]
urlpatterns = [
    path("notifications/", include(notification_patterns)),
]
