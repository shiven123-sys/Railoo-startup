import uuid

from django.conf import settings
from django.db import models

from restrooms.models import Restroom


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    restroom = models.ForeignKey(Restroom, on_delete=models.PROTECT, related_name="bookings")

    pnr_number = models.CharField(max_length=10, blank=True, db_index=True)
    train_number = models.CharField(max_length=10, blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    scheduled_time = models.DateTimeField()
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["pnr_number"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking {self.id} - {self.restroom.name} ({self.status})"
