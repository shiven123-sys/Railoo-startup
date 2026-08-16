from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EmergencyContact, SOSIncident
from .serializers import EmergencyContactSerializer, SOSIncidentSerializer
from .services import notify_emergency_contacts


class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SOSIncidentViewSet(viewsets.ModelViewSet):
    """
    The big red button lives here. `create` fires an incident AND notifies
    every emergency contact the user has on file.
    """

    serializer_class = SOSIncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "incident_type"]

    def get_queryset(self):
        return SOSIncident.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        incident = serializer.save(user=self.request.user)
        notify_emergency_contacts(incident)

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        incident = self.get_object()
        incident.status = SOSIncident.Status.RESOLVED
        incident.resolved_at = timezone.now()
        incident.save(update_fields=["status", "resolved_at"])
        return Response(SOSIncidentSerializer(incident).data)
