from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from restaurant.views import admin_dashboard


urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("", include("restaurant.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
