import django_filters as filters

from .models import Restroom


class RestroomFilter(filters.FilterSet):
    min_cleanliness = filters.NumberFilter(field_name="cleanliness_rating", lookup_expr="gte")
    station_code = filters.CharFilter(field_name="station_code", lookup_expr="iexact")

    class Meta:
        model = Restroom
        fields = {
            "restroom_type": ["exact"],
            "is_women_only": ["exact"],
            "is_wheelchair_accessible": ["exact"],
            "has_baby_care": ["exact"],
            "has_ev_charging": ["exact"],
            "has_fuel_station": ["exact"],
            "has_restaurant": ["exact"],
            "has_parking": ["exact"],
            "is_paid": ["exact"],
        }
