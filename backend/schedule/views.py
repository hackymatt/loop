from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from utils.permissions.permissions import IsLecturer
from schedule.serializers import (
    ManageScheduleSerializer,
    ManageScheduleGetSerializer,
    ScheduleSerializer,
    ScheduleAvailableDateSerializer,
)
from schedule.filters import ScheduleFilter, ScheduleAvailableDateFilter
from schedule.models import Schedule
from schedule.utils import MeetingManager
from profile.models import Profile
from reservation.models import Reservation
from pytz import timezone, utc
from mailer.mailer import Mailer
from django.db.models import F
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from const import CANCELLATION_TIME
from notification.utils import notify
import urllib.parse


class ManageScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Schedule.objects.all()
    serializer_class = ManageScheduleSerializer
    filterset_class = ScheduleFilter
    permission_classes = [IsAuthenticated, IsLecturer]

    def get_serializer_class(self):
        if self.action == "list":
            return ManageScheduleGetSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        lecturer = Profile.objects.get(user=user)
        return self.queryset.filter(lecturer__profile=lecturer)

    def destroy(self, request, *args, **kwargs):
        schedule = super().get_object()

        if (make_aware(datetime.now()) - schedule.start_time) > timedelta(
            microseconds=0
        ):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Nie można odwołać już lekcji."},
            )

        lesson = schedule.lesson
        meeting = schedule.meeting
        profiles = [
            reservation.student.profile
            for reservation in Reservation.objects.filter(schedule=schedule).all()
        ]

        deletion = super().destroy(request, *args, **kwargs)

        if lesson is not None:
            mailer = Mailer()
            # notify students
            start_time = (
                schedule.start_time.replace(tzinfo=utc)
                .astimezone(timezone("Europe/Warsaw"))
                .strftime("%d-%m-%Y %H:%M")
            )
            lecturer_full_name = f"{schedule.lecturer.profile.user.first_name} {schedule.lecturer.profile.user.last_name}"
            data = {
                **{
                    "lesson_title": lesson.title,
                    "lecturer_full_name": lecturer_full_name,
                    "lesson_start_time": start_time,
                }
            }
            for profile in profiles:
                mailer.send(
                    email_template="cancel_lesson.html",
                    to=[profile.user.email],
                    subject="Twoja lekcja została odwołana",
                    data=data,
                )
                notify(
                    profile=profile,
                    title="Twoja lekcja została odwołana",
                    subtitle=lesson.title,
                    description=f"Przepraszamy za zmianę planów. Lekcja, która planowo miała się odbyć {start_time} (PL) została odwołana przez prowadzącego {lecturer_full_name}.",
                    path=f"/account/lessons?sort_by=-created_at&page_size=10&lesson_title={urllib.parse.quote_plus(schedule.lesson.title)}",
                    icon="mdi:calendar-remove",
                )

            if meeting:
                meeting_manager = MeetingManager()
                meeting_manager.delete(event_id=schedule.meeting.event_id)

        return deletion


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Schedule.objects.annotate(
        diff=make_aware(datetime.now()) - F("start_time")
    ).exclude(lesson__isnull=True, diff__gte=-timedelta(hours=CANCELLATION_TIME))
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilter
    permission_classes = [AllowAny]


class ScheduleAvailableDateViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        Schedule.objects.annotate(diff=make_aware(datetime.now()) - F("start_time"))
        .exclude(lesson__isnull=True, diff__gte=-timedelta(hours=CANCELLATION_TIME))
        .annotate(date=TruncDate(F("start_time")))
        .values("date")
        .distinct()
        .order_by()
    )
    serializer_class = ScheduleAvailableDateSerializer
    filterset_class = ScheduleAvailableDateFilter
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
