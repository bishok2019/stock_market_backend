from django.urls import include, path

from .views import (
    CustomUserSignUpAPIView,
    LoginView,
    LogoutView,
    UserNotificationListAPIView,
    UserNotificationRetrieveAPIView,
    UserProfileGetAPIView,
    UserProfileUpdateAPIView,
)

profile_patterns = [
    path("get", UserProfileGetAPIView.as_view(), name="get-profile"),
    path("update", UserProfileUpdateAPIView.as_view(), name="update-profile"),
]
notification_patterns = [
    path(
        "retrieve/<int:pk>",
        UserNotificationRetrieveAPIView.as_view(),
        name="retrieve-user-notification",
    ),
    path(
        "list",
        UserNotificationListAPIView.as_view(),
        name="list-user-notification",
    ),
]
user_pattern = [
    path("signup", CustomUserSignUpAPIView.as_view(), name="signup-user"),
    path("login", LoginView.as_view(), name="login-user"),
    path("logout", LogoutView.as_view(), name="logout-user"),
    path("profile/", include(profile_patterns)),
    path("notification/", include(notification_patterns)),
]

urlpatterns = [
    path("user/", include(user_pattern)),
]
