from django.urls import include, path

urlpatterns = [
    path("", include("apps.catalog.api.urls")),
]
