import uuid

from django.db import models


class PinkHelpPoint(models.Model):
    """A staffed or camera-covered help desk for women travellers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location_description = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_number = models.CharField(max_length=15, blank=True)
    is_staffed_24x7 = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["latitude", "longitude"])]
        ordering = ["name"]

    def __str__(self):
        return self.name


class PeriodCareLocation(models.Model):
    class Category(models.TextChoices):
        VENDING_MACHINE = "VENDING_MACHINE", "Pad Vending Machine"
        MEDICAL_STORE = "MEDICAL_STORE", "Medical Store"
        PHARMACY = "PHARMACY", "Pharmacy"
        WOMEN_CARE_CENTER = "WOMEN_CARE_CENTER", "Women Care Center"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_number = models.CharField(max_length=15, blank=True)
    is_24_hours = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["latitude", "longitude"]),
        ]
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
