from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.core.views import HealthCheckView

urlpatterns = [
    path("secret-panel/", admin.site.urls),
    path("api/health/", HealthCheckView.as_view(), name="health_check"),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Apps
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/admin/orders/", include("apps.orders.api.admin_urls")),
]
