from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from bookings.models import Booking
from restrooms.models import Restroom
from sos.models import SOSIncident
from women_safety.models import PeriodCareLocation, PinkHelpPoint


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = {
            "verified_restrooms": Restroom.objects.filter(is_verified=True, is_active=True).count(),
            "railway_stations_covered": (
                Restroom.objects.filter(restroom_type=Restroom.RestroomType.RAILWAY)
                .exclude(station_code="")
                .values("station_code")
                .distinct()
                .count()
            ),
            "pink_help_points": PinkHelpPoint.objects.filter(is_active=True).count(),
        }
        ctx["top_rated"] = Restroom.objects.filter(is_active=True).order_by("-cleanliness_rating")[:6]
        return ctx


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["recent_bookings"] = (
            Booking.objects.filter(user=user).select_related("restroom")[:5]
        )
        ctx["active_sos"] = SOSIncident.objects.filter(user=user, status=SOSIncident.Status.ACTIVE)
        ctx["emergency_contact_count"] = user.emergency_contacts.count()
        return ctx


class HighwayMapView(TemplateView):
    template_name = "core/highway_map.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["highway_restrooms"] = Restroom.objects.filter(
            restroom_type=Restroom.RestroomType.HIGHWAY, is_active=True
        )[:100]
        return ctx


class SOSView(LoginRequiredMixin, TemplateView):
    template_name = "core/sos.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["emergency_contacts"] = self.request.user.emergency_contacts.all()
        ctx["active_incident"] = (
            SOSIncident.objects.filter(user=self.request.user, status=SOSIncident.Status.ACTIVE).first()
        )
        return ctx


class WomensSafetyView(TemplateView):
    template_name = "core/womens_safety.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["help_points"] = PinkHelpPoint.objects.filter(is_active=True)[:50]
        ctx["period_care_locations"] = PeriodCareLocation.objects.filter(is_active=True)[:50]
        return ctx
