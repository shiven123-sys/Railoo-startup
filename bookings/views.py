from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """A user only ever sees and manages their own bookings."""

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "restroom"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("restroom")

    def perform_create(self, serializer):
        serializer.save(status=Booking.Status.CONFIRMED)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])
        return Response(BookingSerializer(booking).data)
