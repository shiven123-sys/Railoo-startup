from rest_framework import serializers

from .models import EmergencyContact, SOSIncident


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ("id", "name", "phone_number", "relation", "created_at")
        read_only_fields = ("id", "created_at")


class SOSIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOSIncident
        fields = (
            "id", "incident_type", "mode_of_transport", "status",
            "latitude", "longitude", "description",
            "created_at", "resolved_at",
        )
        read_only_fields = ("id", "status", "created_at", "resolved_at")
