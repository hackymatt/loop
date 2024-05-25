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
from pytz import timezone, utc
from mailer.mailer import Mailer


class ProfileUnregisterViewSet(ModelViewSet):
    http_method_names = ["delete"]
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ~IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        user_type = profile.user_type

        mailer = Mailer()

        now = make_aware(datetime.now())
        if user_type[0] == "S":
            dummy_user = User.objects.get(email=settings.DUMMY_STUDENT_EMAIL)
            dummy_profile = Profile.objects.get(user=dummy_user)
            past_reservations = Reservation.objects.filter(
                student=profile, schedule__start_time__lt=now
            )
            past_reservations.update(student=dummy_profile)
            future_reservations_schedules = (
                Reservation.objects.filter(
                    student=profile, schedule__start_time__gte=now
                )
                .values("schedule")
                .distinct()
            )

            for schedule in future_reservations_schedules:
                schedule_obj = Schedule.objects.get(pk=schedule["schedule"])
                other_reservations = Reservation.objects.filter(
                    schedule=schedule_obj
                ).exclude(student=profile)
                if other_reservations.count() == 0:
                    # notify lecturer
                    data = {
                        **{
                            "lesson_title": schedule_obj.lesson.title,
                            "lesson_start_time": schedule_obj.start_time.replace(
                                tzinfo=utc
                            )
                            .astimezone(timezone("Europe/Warsaw"))
                            .strftime("%d-%m-%Y %H:%M"),
                        }
                    }
                    mailer.send(
                        email_template="unreserve_timeslot.html",
                        to=[schedule_obj.lecturer.user.email],
                        subject="Odwołanie rezerwacji terminu.",
                        data=data,
                    )
                    schedule_obj.lesson = None
                    schedule_obj.save()
        else:
            dummy_user = User.objects.get(email=settings.DUMMY_LECTURER_EMAIL)
            dummy_profile = Profile.objects.get(user=dummy_user)
            past_schedules = Schedule.objects.filter(
                lecturer=profile, start_time__lt=now, lesson__isnull=False
            )
            past_schedules.update(lecturer=dummy_profile)
            future_schedules = Schedule.objects.filter(
                lecturer=profile, start_time__gte=now, lesson__isnull=False
            )
            for schedule in future_schedules:
                emails = [
                    reservation.student.user.email
                    for reservation in Reservation.objects.filter(
                        schedule=schedule
                    ).all()
                ]
                # notify students
                data = {
                    **{
                        "lesson_title": schedule.lesson.title,
                        "lecturer_full_name": f"{schedule.lecturer.user.first_name} {schedule.lecturer.user.last_name}",
                        "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                        .astimezone(timezone("Europe/Warsaw"))
                        .strftime("%d-%m-%Y %H:%M"),
                    }
                }
                for email in emails:
                    mailer.send(
                        email_template="cancel_lesson.html",
                        to=[email],
                        subject="Twoja lekcja została odwołana.",
                        data=data,
                    )

        user.delete()

        return Response({})
