from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restroom", "status", "scheduled_time", "amount", "is_paid", "created_at")
    list_filter = ("status", "is_paid")
    search_fields = ("id", "user__username", "restroom__name", "pnr_number")
    readonly_fields = ("created_at", "updated_at")
