from django.contrib import admin

from .models import PeriodCareLocation, PinkHelpPoint


@admin.register(PinkHelpPoint)
class PinkHelpPointAdmin(admin.ModelAdmin):
    list_display = ("name", "is_staffed_24x7", "contact_number", "is_active")
    list_filter = ("is_staffed_24x7", "is_active")
    search_fields = ("name", "location_description")


@admin.register(PeriodCareLocation)
class PeriodCareLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_24_hours", "contact_number", "is_active")
    list_filter = ("category", "is_24_hours", "is_active")
    search_fields = ("name",)
