from django.contrib import admin

from .models import EmergencyContact, SOSIncident


@admin.register(SOSIncident)
class SOSIncidentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "incident_type", "mode_of_transport", "status", "created_at", "resolved_at")
    list_filter = ("incident_type", "mode_of_transport", "status")
    search_fields = ("user__username", "description")
    readonly_fields = ("created_at",)


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "phone_number", "relation")
    search_fields = ("name", "user__username", "phone_number")
