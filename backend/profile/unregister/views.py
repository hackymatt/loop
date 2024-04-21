from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
from profile.models import Profile
from reservation.models import Reservation
from schedule.models import Schedule
from datetime import datetime
from django.utils.timezone import make_aware


class ProfileUnregisterViewSet(ModelViewSet):
    http_method_names = ["delete"]
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ~IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        user_type = profile.user_type

        if user_type[0] == "S":
            dummy_user = User.objects.get(email=settings.DUMMY_STUDENT_EMAIL)
            dummy_profile = Profile.objects.get(user=dummy_user)
            reservations = Reservation.objects.filter(
                student=profile, schedule__start_time__lte=make_aware(datetime.now())
            )
            reservations.update(student=dummy_profile)
        else:
            dummy_user = User.objects.get(email=settings.DUMMY_LECTURER_EMAIL)
            dummy_profile = Profile.objects.get(user=dummy_user)
            schedules = Schedule.objects.filter(
                lecturer=profile, start_time__lte=make_aware(datetime.now())
            )
            schedules.update(lecturer=dummy_profile)

        user.delete()

        return Response({})
