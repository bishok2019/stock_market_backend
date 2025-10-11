from django.urls import include, path

urlpatterns = [
    path("auth-app/", include("apps.authentication.urls")),
    path("stock-app/", include("apps.stock.urls")),
]
