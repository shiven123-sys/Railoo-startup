from rest_framework.routers import DefaultRouter

from . import views

app_name = "bookings"

router = DefaultRouter()
router.register("", views.BookingViewSet, basename="booking")

urlpatterns = router.urls
