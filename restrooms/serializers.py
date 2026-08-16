from rest_framework import serializers

from .models import Restroom, RestroomRating


class RestroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restroom
        fields = (
            "id", "name", "restroom_type",
            "station_name", "station_code", "platform_number",
            "highway_name", "landmark",
            "latitude", "longitude",
            "is_women_only", "is_wheelchair_accessible", "has_baby_care",
            "has_ev_charging", "has_fuel_station", "has_restaurant", "has_parking",
            "is_paid", "price",
            "cleanliness_rating", "total_ratings",
            "is_verified", "is_active",
            "created_at",
        )
        read_only_fields = ("id", "cleanliness_rating", "total_ratings", "is_verified", "created_at")


class RestroomRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RestroomRating
        fields = (
            "id", "restroom", "user",
            "cleanliness_score", "safety_score", "overall_score",
            "comment", "created_at",
        )
        read_only_fields = ("id", "user", "created_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
