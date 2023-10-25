from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

API_PATTERNS = [
    path("auth/", include("users.urls")),
    path("auth/", include("config.urls.jwt")),
    path("blog/", include("blog.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(API_PATTERNS)),
]

if settings.DEBUG:
    urlpatterns = [
        path("", include("config.urls.swagger")),
        path("__debug__/", include("debug_toolbar.urls")),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        *urlpatterns,
    ]
