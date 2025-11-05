from django.urls import include, path

from .views import (
    CustomUserSignUpAPIView,
    LoginView,
    LogoutView,
    UserProfileGetAPIView,
    UserProfileUpdateAPIView,
)

profile_patterns = [
    path("get", UserProfileGetAPIView.as_view(), name="get-profile"),
    path("update", UserProfileUpdateAPIView.as_view(), name="update-profile"),
]
user_pattern = [
    path("signup", CustomUserSignUpAPIView.as_view(), name="signup-user"),
    path("login", LoginView.as_view(), name="login-user"),
    path("logout", LogoutView.as_view(), name="logout-user"),
    path("profile/", include(profile_patterns)),
]

urlpatterns = [
    path("user/", include(user_pattern)),
]
