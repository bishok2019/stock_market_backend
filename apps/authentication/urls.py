from django.urls import include, path

from .views import CustomUserSignUpAPIView, LoginView, LogoutView

urlpatterns = [
    path("user/signup", CustomUserSignUpAPIView.as_view(), name="signup-user"),
    path("user/login", LoginView.as_view(), name="login-user"),
    path("user/logout", LogoutView.as_view(), name="logout-user"),
]
