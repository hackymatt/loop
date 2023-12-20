from rest_framework.serializers import ModelSerializer
from purchase.models import CoursePurchase, LessonPurchase
from course.models import Course, Lesson, Technology


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    technology = TechnologySerializer()

    class Meta:
        model = Course
        exclude = (
            "description",
            "github_url",
            "price",
            "active",
            "skills",
            "topics",
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
        exclude = ("student",)


class PurchaseSerializer(ModelSerializer):
    course_purchase = CoursePurchaseSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = LessonPurchase
        exclude = ("student",)
