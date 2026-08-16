from rest_framework import serializers

from restrooms.serializers import RestroomSerializer

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    restroom_detail = RestroomSerializer(source="restroom", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id", "restroom", "restroom_detail",
            "pnr_number", "train_number",
            "status", "scheduled_time", "amount", "is_paid",
            "created_at",
        )
        read_only_fields = ("id", "status", "is_paid", "created_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["amount"] = validated_data["restroom"].price
        return super().create(validated_data)
