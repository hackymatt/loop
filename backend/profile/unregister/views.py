from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from profile.models import Profile, LecturerProfile, StudentProfile
from reservation.models import Reservation
from schedule.models import Schedule
from datetime import datetime
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from notification.utils import notify
from urllib.parse import quote_plus
from config_global import DUMMY_STUDENT_EMAIL, DUMMY_LECTURER_EMAIL


class ProfileUnregisterViewSet(ModelViewSet):
    http_method_names = ["delete"]
    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAuthenticated, ~IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        user_type = profile.user_type

        mailer = Mailer()

        now = make_aware(datetime.now())
        if user_type[0] == "S":
            dummy_profile = Profile.objects.get(user__email=DUMMY_STUDENT_EMAIL)
            past_reservations = Reservation.objects.filter(
                student__profile=profile, schedule__start_time__lt=now
            )
            past_reservations.update(
                student=StudentProfile.objects.get(profile=dummy_profile)
            )
            future_reservations_schedules = (
                Reservation.objects.filter(
                    student__profile=profile, schedule__start_time__gte=now
                )
                .values("schedule")
                .distinct()
            )

            for schedule in future_reservations_schedules:
                schedule_obj = Schedule.objects.get(pk=schedule["schedule"])
                other_reservations = Reservation.objects.filter(
                    schedule=schedule_obj
                ).exclude(student__profile=profile)
                start_time = (
                    schedule_obj.start_time.replace(tzinfo=utc)
                    .astimezone(timezone("Europe/Warsaw"))
                    .strftime("%d-%m-%Y %H:%M")
                )
                if other_reservations.count() == 0:
                    # notify lecturer
                    data = {
                        **{
                            "lesson_title": schedule_obj.lesson.title,
                            "lesson_start_time": start_time,
                        }
                    }
                    mailer.send(
                        email_template="cancel_timeslot.html",
                        to=[schedule_obj.lecturer.profile.user.email],
                        subject="Odwołanie rezerwacji terminu",
                        data=data,
                    )
                    notify(
                        profile=schedule_obj.lecturer.profile,
                        title="Odwołanie rezerwacji terminu",
                        subtitle=schedule_obj.lesson.title,
                        description=f"Przepraszamy za zmianę planów. Lekcja, która planowo miała się odbyć {start_time} (PL) została odwołana.",
                        path=f"/account/teacher/calendar?time_from={schedule_obj.start_time.strftime('%Y-%m-%d')}&view=day",
                        icon="mdi:calendar-remove",
                    )
                    schedule_obj.lesson = None
                    schedule_obj.save()
        else:
            dummy_profile = Profile.objects.get(user__email=DUMMY_LECTURER_EMAIL)
            past_schedules = Schedule.objects.filter(
                lecturer__profile=profile, start_time__lt=now, lesson__isnull=False
            )
            past_schedules.update(
                lecturer=LecturerProfile.objects.get(profile=dummy_profile)
            )
            future_schedules = Schedule.objects.filter(
                lecturer__profile=profile, start_time__gte=now, lesson__isnull=False
            )
            for schedule in future_schedules:
                profiles = [
                    reservation.student.profile
                    for reservation in Reservation.objects.filter(
                        schedule=schedule
                    ).all()
                ]
                start_time = (
                    schedule.start_time.replace(tzinfo=utc)
                    .astimezone(timezone("Europe/Warsaw"))
                    .strftime("%d-%m-%Y %H:%M")
                )
                lecturer_full_name = f"{schedule.lecturer.profile.user.first_name} {schedule.lecturer.profile.user.last_name}"
                # notify students
                data = {
                    **{
                        "lesson_title": schedule.lesson.title,
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
                        subtitle=schedule.lesson.title,
                        description=f"Przepraszamy za zmianę planów. Lekcja, która planowo miała się odbyć {start_time} (PL) została odwołana przez prowadzącego {lecturer_full_name}.",
                        path=f"/account/lessons?sort_by=-created_at&page_size=10&lesson_title={quote_plus(schedule.lesson.title)}",
                        icon="mdi:calendar-remove",
                    )

        user.delete()

        return Response({})
