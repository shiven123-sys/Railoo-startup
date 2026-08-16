import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Restroom(models.Model):
    class RestroomType(models.TextChoices):
        RAILWAY = "RAILWAY", "Railway Station"
        HIGHWAY = "HIGHWAY", "Highway"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    restroom_type = models.CharField(max_length=10, choices=RestroomType.choices, db_index=True)

    # Railway context
    station_name = models.CharField(max_length=150, blank=True, db_index=True)
    station_code = models.CharField(max_length=10, blank=True, db_index=True)
    platform_number = models.CharField(max_length=10, blank=True)

    # Highway context
    highway_name = models.CharField(max_length=150, blank=True, db_index=True)
    landmark = models.CharField(max_length=200, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Amenity flags
    is_women_only = models.BooleanField(default=False)
    is_wheelchair_accessible = models.BooleanField(default=False)
    has_baby_care = models.BooleanField(default=False)
    has_ev_charging = models.BooleanField(default=False)
    has_fuel_station = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)

    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    cleanliness_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Denormalized average of RestroomRating.cleanliness_score for fast list/filter queries.",
    )
    total_ratings = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["restroom_type", "is_active"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["cleanliness_rating"]),
        ]
        ordering = ["-cleanliness_rating", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_restroom_type_display()})"

    def recalculate_rating(self):
        """Refresh the denormalized rating fields from related RestroomRating rows."""
        agg = self.ratings.aggregate(models.Avg("cleanliness_score"), models.Count("id"))
        self.cleanliness_rating = agg["cleanliness_score__avg"] or 0
        self.total_ratings = agg["id__count"] or 0
        self.save(update_fields=["cleanliness_rating", "total_ratings", "updated_at"])


class RestroomRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restroom = models.ForeignKey(Restroom, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restroom_ratings")

    cleanliness_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    safety_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    overall_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["restroom", "user"], name="one_rating_per_user_per_restroom"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.restroom.name} rated {self.overall_score}/5 by {self.user}"
