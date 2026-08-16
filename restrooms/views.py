from dataclasses import asdict

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RestroomFilter
from .models import Restroom, RestroomRating
from .serializers import RestroomRatingSerializer, RestroomSerializer
from .services import PNRLookupService


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class RestroomViewSet(viewsets.ModelViewSet):
    """
    Browse and manage restrooms. Read access is public (so the map/landing
    page can show real data before login); write access requires auth and
    should be limited to staff in production via a custom permission.
    """

    queryset = Restroom.objects.filter(is_active=True)
    serializer_class = RestroomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = RestroomFilter
    search_fields = ["name", "station_name", "highway_name", "landmark"]
    ordering_fields = ["cleanliness_rating", "price", "created_at"]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def rate(self, request, pk=None):
        restroom = self.get_object()
        serializer = RestroomRatingSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(restroom=restroom)
        restroom.recalculate_rating()
        return Response(RestroomSerializer(restroom).data, status=201)


class RestroomRatingViewSet(viewsets.ModelViewSet):
    queryset = RestroomRating.objects.all()
    serializer_class = RestroomRatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ["restroom"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PNRLookupView(APIView):
    """GET /api/v1/restrooms/pnr/<pnr>/ -> route + restrooms at each upcoming station."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, pnr: str):
        route = PNRLookupService.get_train_route(pnr)
        stations_payload = []
        for station in route.upcoming_stations:
            restrooms = Restroom.objects.filter(
                restroom_type=Restroom.RestroomType.RAILWAY,
                station_code__iexact=station.code,
                is_active=True,
            )
            stations_payload.append(
                {
                    **asdict(station),
                    "restrooms": RestroomSerializer(restrooms, many=True).data,
                }
            )

        return Response(
            {
                "pnr": route.pnr,
                "train_number": route.train_number,
                "train_name": route.train_name,
                "current_station": route.current_station,
                "upcoming_stations": stations_payload,
            }
        )
