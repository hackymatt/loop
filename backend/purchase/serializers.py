from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    EmailField,
    CharField,
    ImageField,
)
from purchase.models import Purchase
from course.models import Course
from lesson.models import Lesson, Technology
from profile.models import Profile
from reservation.models import Reservation
from review.models import Review
from datetime import datetime
from django.utils.timezone import make_aware


def get_review(purchase):
    return Review.objects.filter(student=purchase.student, lesson=purchase.lesson)


def get_reservation(purchase):
    return Reservation.objects.filter(student=purchase.student, lesson=purchase.lesson)


class LessonStatus:
    NEW = "nowa"
    PLANNED = "zaplanowana"
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


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        exclude = (
            "technology",
            "level",
            "image",
            "video",
            "description",
            "price",
            "active",
            "skills",
            "topics",
            "modified_at",
            "created_at",
        )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        exclude = (
            "description",
            "duration",
            "price",
            "active",
            "modified_at",
            "created_at",
        )


class ProfileSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="user.email")
    gender = CharField(source="get_gender_display")
    image = ImageField()

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "full_name",
            "email",
            "gender",
            "image",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


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


class PurchaseGetSerializer(ModelSerializer):
    course = CourseSerializer(source="course_purchase.course")
    lesson = LessonSerializer()
    lesson_status = SerializerMethodField("get_lesson_status")
    lecturer = SerializerMethodField("get_lecturer")
    review_status = SerializerMethodField("get_review_status")
    review = SerializerMethodField("get_review_details")

    class Meta:
        model = Purchase
        exclude = (
            "student",
            "modified_at",
            "course_purchase",
        )

    def get_lesson_status(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            schedule_time = reservation.first().schedule.time
            if make_aware(datetime.now()) >= schedule_time:
                return LessonStatus.COMPLETED
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

    def get_lecturer(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            return ProfileSerializer(
                reservation.first().schedule.lecturer,
                context={"request": self.context.get("request")},
            ).data
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
        exclude = (
            "course_purchase",
            "student",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        student = Profile.objects.get(user=user)

        return Purchase.objects.create(
            **validated_data,
            student=student,
        )
