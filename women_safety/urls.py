from rest_framework.routers import DefaultRouter

from . import views

app_name = "women_safety"

router = DefaultRouter()
router.register("help-points", views.PinkHelpPointViewSet, basename="help-point")
router.register("period-care", views.PeriodCareLocationViewSet, basename="period-care")

urlpatterns = router.urls
