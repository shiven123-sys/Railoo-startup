from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "phone_number", "is_women_safety_verified", "is_staff", "created_at")
    list_filter = ("is_staff", "is_active", "is_women_safety_verified")
    search_fields = ("username", "email", "phone_number")
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Railoo profile",
            {
                "fields": (
                    "phone_number",
                    "date_of_birth",
                    "profile_picture",
                    "is_women_safety_verified",
                    "emergency_contact_name",
                    "emergency_contact_phone",
                )
            },
        ),
    )
