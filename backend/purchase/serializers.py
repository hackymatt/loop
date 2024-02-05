from rest_framework.serializers import ModelSerializer, SerializerMethodField
from purchase.models import CoursePurchase, LessonPurchase
from course.models import Course, Lesson, Technology
from profile.models import Profile
from reservation.models import Reservation
from datetime import datetime
from django.utils.timezone import make_aware


class PurchaseStatus:
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )


class CourseSerializer(ModelSerializer):
    technology = TechnologySerializer(many=True)

    class Meta:
        model = Course
        exclude = (
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
        )


class CoursePurchaseSerializer(ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CoursePurchase
        exclude = (
            "student",
            "modified_at",
            "created_at",
        )


class PurchaseGetSerializer(ModelSerializer):
    course_purchase = CoursePurchaseSerializer()
    lesson = LessonSerializer()
    status = SerializerMethodField("get_status")

    class Meta:
        model = LessonPurchase
        exclude = (
            "student",
            "modified_at",
        )

    def get_status(self, purchase):
        reservation = Reservation.objects.filter(
            student=purchase.student, lesson=purchase.lesson
        )

        if reservation.exists():
            schedule_time = reservation.first().schedule.time
            if make_aware(datetime.now()) >= schedule_time:
                return PurchaseStatus.COMPLETED
            else:
                return PurchaseStatus.IN_PROGRESS
        else:
            return PurchaseStatus.NEW


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
