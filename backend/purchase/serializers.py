from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ImageField,
    ValidationError,
)
from django.db.models import Prefetch
from purchase.models import Purchase, Payment
from lesson.models import Lesson, Technology
from profile.models import Profile, LecturerProfile, StudentProfile
from reservation.models import Reservation
from schedule.models import Schedule, Recording
from review.models import Review


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
    full_name = SerializerMethodField()
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

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


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
    lesson_status = SerializerMethodField()
    reservation = SerializerMethodField()
    review_status = SerializerMethodField()
    review = SerializerMethodField()
    meeting_url = SerializerMethodField()
    recordings = SerializerMethodField()

    class Meta:
        model = Purchase
        exclude = (
            "student",
            "modified_at",
        )

    def get_meeting_url(self, purchase: Purchase):
        return purchase.meeting_url

    def get_recordings(self, purchase: Purchase):
        if purchase.recordings_ids == []:
            return None
        recordings = Recording.objects.filter(id__in=purchase.recordings_ids)
        return RecordingSerializer(recordings, many=True).data

    def get_lesson_status(self, purchase: Purchase):
        return purchase.lesson_status

    def get_review_status(self, purchase: Purchase):
        return purchase.review_status

    def get_reservation(self, purchase: Purchase):
        if not purchase.reservation_id:
            return None

        reservation = Reservation.objects.prefetch_related(
            Prefetch(
                "schedule__lecturer", queryset=LecturerProfile.objects.add_full_name()
            )
        ).get(id=purchase.reservation_id)
        return ReservationSerializer(reservation).data

    def get_review(self, purchase: Purchase):
        if not purchase.review_id:
            return None

        review = Review.objects.get(id=purchase.review_id)
        return ReviewSerializer(review).data


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


class PaymentSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Payment
        exclude = (
            "id",
            "created_at",
            "modified_at",
        )
