from django.contrib import admin

from .models import Restroom, RestroomRating


class RestroomRatingInline(admin.TabularInline):
    model = RestroomRating
    extra = 0
    readonly_fields = ("user", "cleanliness_score", "safety_score", "overall_score", "comment", "created_at")
    can_delete = False


@admin.register(Restroom)
class RestroomAdmin(admin.ModelAdmin):
    list_display = (
        "name", "restroom_type", "station_name", "highway_name",
        "cleanliness_rating", "total_ratings", "is_women_only",
        "is_wheelchair_accessible", "is_verified", "is_active",
    )
    list_filter = (
        "restroom_type", "is_women_only", "is_wheelchair_accessible",
        "has_baby_care", "has_ev_charging", "is_verified", "is_active",
    )
    search_fields = ("name", "station_name", "station_code", "highway_name", "landmark")
    readonly_fields = ("cleanliness_rating", "total_ratings", "created_at", "updated_at")
    inlines = [RestroomRatingInline]


@admin.register(RestroomRating)
class RestroomRatingAdmin(admin.ModelAdmin):
    list_display = ("restroom", "user", "overall_score", "cleanliness_score", "safety_score", "created_at")
    list_filter = ("overall_score",)
    search_fields = ("restroom__name", "user__username")
