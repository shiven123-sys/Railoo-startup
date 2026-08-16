from rest_framework import permissions, viewsets

from .models import PeriodCareLocation, PinkHelpPoint
from .serializers import PeriodCareLocationSerializer, PinkHelpPointSerializer


class PinkHelpPointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PinkHelpPoint.objects.filter(is_active=True)
    serializer_class = PinkHelpPointSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "location_description"]


class PeriodCareLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PeriodCareLocation.objects.filter(is_active=True)
    serializer_class = PeriodCareLocationSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["category", "is_24_hours"]
    search_fields = ["name"]
