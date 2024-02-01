from rest_framework.serializers import ModelSerializer
from purchase.models import CoursePurchase, LessonPurchase
from course.models import Course, Lesson, Technology
from profile.models import Profile


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


class PurchaseGetSerializer(ModelSerializer):
    course_purchase = CoursePurchaseSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = LessonPurchase
        exclude = ("student",)


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
