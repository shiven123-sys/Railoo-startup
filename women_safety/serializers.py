from rest_framework import serializers

from .models import PeriodCareLocation, PinkHelpPoint


class PinkHelpPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinkHelpPoint
        fields = (
            "id", "name", "location_description", "latitude", "longitude",
            "contact_number", "is_staffed_24x7", "is_active",
        )


class PeriodCareLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodCareLocation
        fields = (
            "id", "name", "category", "latitude", "longitude",
            "contact_number", "is_24_hours", "is_active",
        )
