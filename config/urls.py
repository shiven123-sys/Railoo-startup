from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Server-rendered pages
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),

    # Versioned JSON API
    path("api/v1/auth/", include("accounts.api_urls")),
    path("api/v1/restrooms/", include("restrooms.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
    path("api/v1/sos/", include("sos.urls")),
    path("api/v1/women-safety/", include("women_safety.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
