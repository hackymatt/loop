from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    CharField,
    ImageField,
    URLField,
    ValidationError,
)
from purchase.models import Purchase, Payment
from lesson.models import Lesson, Technology
from profile.models import Profile, LecturerProfile, StudentProfile
from reservation.models import Reservation
from schedule.models import Schedule, Recording
from review.models import Review
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from config_global import CANCELLATION_TIME


def get_review(purchase):
    return Review.objects.filter(student=purchase.student, lesson=purchase.lesson)


def get_reservation(purchase):
    return Reservation.objects.filter(purchase=purchase)


class LessonStatus:
    NEW = "nowa"
    PLANNED = "zaplanowana"
    CONFIRMED = "potwierdzona"
    COMPLETED = "zakończona"


class ReviewStatus:
    NOT_COMPLETED = "oczekujące"
    COMPLETED = "ukończone"
    NONE = "brak"


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        exclude = (
            "active",
            "technologies",
            "description",
            "price",
            "modified_at",
            "created_at",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = (
            "student",
            "lecturer",
            "modified_at",
            "created_at",
            "lesson",
        )


class ScheduleSerializer(ModelSerializer):
    lecturer = LecturerSerializer()

    class Meta:
        model = Schedule
        exclude = (
            "lesson",
            "created_at",
            "modified_at",
        )


class ReservationSerializer(ModelSerializer):
    schedule = ScheduleSerializer()

    class Meta:
        model = Reservation
        exclude = (
            "student",
            "lesson",
            "created_at",
            "modified_at",
        )


class RecordingSerializer(ModelSerializer):
    class Meta:
        model = Recording
        fields = (
            "file_name",
            "file_url",
        )


class PurchaseGetSerializer(ModelSerializer):
    lesson = LessonSerializer()
    lesson_status = SerializerMethodField("get_lesson_status")
    reservation = SerializerMethodField("get_reservation_details")
    review_status = SerializerMethodField("get_review_status")
    review = SerializerMethodField("get_review_details")
    meeting_url = SerializerMethodField("get_meeting_url")
    recordings = SerializerMethodField("get_recordings_url")

    class Meta:
        model = Purchase
        exclude = (
            "student",
            "modified_at",
        )

    def get_meeting_url(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            schedule = reservation.first().schedule
            if (schedule.start_time - make_aware(datetime.now())) < timedelta(
                hours=CANCELLATION_TIME
            ):
                return schedule.meeting.url
            else:
                return None
        else:
            return None

    def get_recordings_url(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            schedule = reservation.first().schedule
            recordings = Recording.objects.filter(schedule=schedule)
            return RecordingSerializer(recordings, many=True).data
        else:
            return []

    def get_lesson_status(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            start_time = reservation.first().schedule.start_time
            end_time = reservation.first().schedule.end_time
            if make_aware(datetime.now()) >= end_time:
                return LessonStatus.COMPLETED
            elif (start_time - make_aware(datetime.now())) < timedelta(
                hours=CANCELLATION_TIME
            ):
                return LessonStatus.CONFIRMED
            else:
                return LessonStatus.PLANNED
        else:
            return LessonStatus.NEW

    def get_review_status(self, purchase):
        lesson_status = self.get_lesson_status(purchase=purchase)

        if lesson_status == LessonStatus.COMPLETED:
            review = get_review(purchase=purchase)

            if review.exists():
                return ReviewStatus.COMPLETED
            else:
                return ReviewStatus.NOT_COMPLETED
        else:
            return ReviewStatus.NONE

    def get_reservation_details(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            return ReservationSerializer(reservation.first()).data
        else:
            return None

    def get_review_details(self, purchase):
        review = get_review(purchase=purchase)

        if review.exists():
            return ReviewSerializer(review.first()).data
        else:
            return None


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        exclude = ("student", "payment")

    def validate_lesson(self, lesson):
        if not lesson.active:
            raise ValidationError("Lekcja jest nieaktywna.")

        return lesson

    def create(self, validated_data):
        user = self.context["request"].user
        student = Profile.objects.get(user=user)

        payment_id = self.context["payment"]
        payment = Payment.objects.get(pk=payment_id)

        objs = []
        for data in validated_data:
            lesson = Lesson.objects.get(id=data["lesson"])
            obj = Purchase.objects.create(
                lesson=lesson,
                price=data["price"],
                student=StudentProfile.objects.get(profile=student),
                payment=payment,
            )
            objs.append(obj)

        return objs
