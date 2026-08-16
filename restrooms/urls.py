from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "restrooms"

router = DefaultRouter()
router.register("ratings", views.RestroomRatingViewSet, basename="rating")
router.register("", views.RestroomViewSet, basename="restroom")

urlpatterns = [
    path("pnr/<str:pnr>/", views.PNRLookupView.as_view(), name="pnr_lookup"),
    path("", include(router.urls)),
]
