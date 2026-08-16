import uuid

from django.conf import settings
from django.db import models


class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emergency_contacts")
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    relation = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.relation}) - {self.user}"


class SOSIncident(models.Model):
    class IncidentType(models.TextChoices):
        MEDICAL = "MEDICAL", "Medical Emergency"
        SAFETY = "SAFETY", "Personal Safety"
        HARASSMENT = "HARASSMENT", "Harassment"
        FIRE = "FIRE", "Fire"
        OTHER = "OTHER", "Other"

    class TransportMode(models.TextChoices):
        TRAIN = "TRAIN", "Train"
        BUS = "BUS", "Bus"
        HIGHWAY = "HIGHWAY", "Highway"
        METRO = "METRO", "Metro"
        CAB = "CAB", "Cab"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RESOLVED = "RESOLVED", "Resolved"
        FALSE_ALARM = "FALSE_ALARM", "False Alarm"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sos_incidents")

    incident_type = models.CharField(max_length=15, choices=IncidentType.choices)
    mode_of_transport = models.CharField(max_length=10, choices=TransportMode.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ACTIVE, db_index=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"SOS #{str(self.id)[:8]} - {self.get_incident_type_display()} ({self.status})"
