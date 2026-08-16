from rest_framework.routers import DefaultRouter

from . import views

app_name = "sos"

router = DefaultRouter()
router.register("contacts", views.EmergencyContactViewSet, basename="emergency-contact")
router.register("incidents", views.SOSIncidentViewSet, basename="incident")

urlpatterns = router.urls
