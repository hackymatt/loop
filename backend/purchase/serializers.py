from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    EmailField,
    CharField,
    ImageField,
)
from purchase.models import CoursePurchase, LessonPurchase
from course.models import Course, Lesson, Technology
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
    NEW = "Nowa"
    PLANNED = "Zaplanowana"
    COMPLETED = "Zakończona"


class ReviewStatus:
    NOT_COMPLETED = "Oczekujące"
    COMPLETED = "Ukończone"


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
            "github_url",
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
            "course",
            "description",
            "duration",
            "github_url",
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
        model = LessonPurchase
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
        review = get_review(purchase=purchase)

        if review.exists():
            return ReviewStatus.COMPLETED
        else:
            return ReviewStatus.NOT_COMPLETED

    def get_lecturer(self, purchase):
        reservation = get_reservation(purchase=purchase)

        if reservation.exists():
            return ProfileSerializer(reservation.first().schedule.lecturer, context={"request": self.context.get("request")}).data
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
        model = LessonPurchase
        exclude = (
            "course_purchase",
            "student",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        student = Profile.objects.get(user=user)

        lesson = validated_data.pop("lesson")

        course_purchase, _ = CoursePurchase.objects.get_or_create(
            course=lesson.course, price=lesson.course.price, student=student
        )

        return LessonPurchase.objects.create(
            **validated_data,
            course_purchase=course_purchase,
            lesson=lesson,
            student=student,
        )
