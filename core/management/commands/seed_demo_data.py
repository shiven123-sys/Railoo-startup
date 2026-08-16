from django.core.management.base import BaseCommand

from restrooms.models import Restroom
from women_safety.models import PeriodCareLocation, PinkHelpPoint


class Command(BaseCommand):
    help = "Seed the database with demo restrooms, help points and period care locations."

    def handle(self, *args, **options):
        railway_data = [
            dict(name="Platform 1 Washroom", station_name="New Delhi", station_code="NDLS",
                 platform_number="1", latitude=28.6430, longitude=77.2194,
                 is_women_only=False, is_wheelchair_accessible=True, has_baby_care=True,
                 is_paid=True, price=10, is_verified=True),
            dict(name="Women's Washroom - Platform 3", station_name="New Delhi", station_code="NDLS",
                 platform_number="3", latitude=28.6432, longitude=77.2198,
                 is_women_only=True, is_wheelchair_accessible=True, has_baby_care=True,
                 is_paid=False, is_verified=True),
            dict(name="Central Washroom", station_name="Lucknow", station_code="LKO",
                 platform_number="2", latitude=26.8393, longitude=80.9231,
                 is_wheelchair_accessible=True, is_paid=True, price=5, is_verified=True),
            dict(name="Howrah Junction Washroom", station_name="Howrah", station_code="HWH",
                 platform_number="9", latitude=22.5839, longitude=88.3425,
                 is_paid=True, price=10, is_verified=True),
        ]

        highway_data = [
            dict(name="Highway Oasis - NH48", highway_name="NH48", landmark="Neemrana",
                 latitude=27.9925, longitude=76.3806,
                 has_fuel_station=True, has_restaurant=True, has_ev_charging=True,
                 has_parking=True, is_wheelchair_accessible=True, is_verified=True),
            dict(name="Highway Rest Stop - NH44", highway_name="NH44", landmark="Ambala",
                 latitude=30.3782, longitude=76.7767,
                 has_fuel_station=True, has_parking=True, is_verified=True),
            dict(name="Family Dhaba & Restroom - NH8", highway_name="NH8", landmark="Kherki Daula",
                 latitude=28.4211, longitude=76.9877,
                 has_restaurant=True, has_parking=True, is_women_only=False,
                 is_wheelchair_accessible=True, is_verified=True),
        ]

        created = 0
        for row in railway_data + highway_data:
            row.setdefault("restroom_type", Restroom.RestroomType.RAILWAY if "station_code" in row else Restroom.RestroomType.HIGHWAY)
            _, was_created = Restroom.objects.get_or_create(
                name=row["name"], defaults=row
            )
            created += int(was_created)

        help_points = [
            dict(name="Pink Help Point - NDLS Concourse", location_description="Near enquiry counter",
                 latitude=28.6430, longitude=77.2194, contact_number="139", is_staffed_24x7=True),
            dict(name="Pink Help Point - Howrah", location_description="Platform 1 entrance",
                 latitude=22.5839, longitude=88.3425, contact_number="139", is_staffed_24x7=False),
        ]
        for row in help_points:
            _, was_created = PinkHelpPoint.objects.get_or_create(name=row["name"], defaults=row)
            created += int(was_created)

        period_care = [
            dict(name="NDLS Pad Vending Machine", category=PeriodCareLocation.Category.VENDING_MACHINE,
                 latitude=28.6430, longitude=77.2194, is_24_hours=True),
            dict(name="Apollo Pharmacy - Lucknow Station Road", category=PeriodCareLocation.Category.PHARMACY,
                 latitude=26.8393, longitude=80.9231, is_24_hours=True, contact_number="1800-123-4567"),
            dict(name="Women Care Center - Howrah", category=PeriodCareLocation.Category.WOMEN_CARE_CENTER,
                 latitude=22.5839, longitude=88.3425, is_24_hours=False),
        ]
        for row in period_care:
            _, was_created = PeriodCareLocation.objects.get_or_create(name=row["name"], defaults=row)
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seed complete — {created} new demo records created."))
