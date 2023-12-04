from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from reservation.serializers import (
    ReservationSerializer,
    ReservationGetSerializer,
)
from reservation.models import Reservation
from profile.models import Profile


class ReservationViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ReservationGetSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)
