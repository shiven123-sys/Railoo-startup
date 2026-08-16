from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model so we can attach Railoo-specific fields (phone,
    emergency contact, women-safety verification) without an awkward
    OneToOne profile table.
    """

    phone_number = models.CharField(max_length=15, blank=True, db_index=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    is_women_safety_verified = models.BooleanField(
        default=False,
        help_text="Set once a user has opted into and verified the Women's Safety module.",
    )
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone_number"]),
        ]

    def __str__(self):
        return self.get_full_name() or self.username
