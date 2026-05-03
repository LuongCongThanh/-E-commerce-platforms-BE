from django.urls import include, path

urlpatterns = [
    path("", include("apps.orders.api.urls")),
]
