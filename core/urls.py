from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("highway/", views.HighwayMapView.as_view(), name="highway_map"),
    path("sos/", views.SOSView.as_view(), name="sos"),
    path("womens-safety/", views.WomensSafetyView.as_view(), name="womens_safety"),
]
