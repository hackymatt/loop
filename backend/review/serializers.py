from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
)
from review.models import Review
from profile.models import Profile
from course.models import Lesson
from purchase.models import LessonPurchase


class BestReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = (
            "lecturer",
            "lesson",
            "rating",
        )


class ProfileSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ReviewGetSerializer(ModelSerializer):
    lesson_title = CharField(source="lesson.title")
    student = ProfileSerializer()
    lecturer = ProfileSerializer()

    class Meta:
        model = Review
        fields = (
            "lesson_title",
            "student",
            "lecturer",
            "rating",
            "review",
            "created_at",
        )


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = ("student",)

    def validate_lesson(self, lesson):
        request_type = self.context["request"].method
        
        if request_type == "PUT":
            return lesson
        
        user = self.context["request"].user
        data = self.context["request"].data
        profile = Profile.objects.get(user=user)
        lecturer = Profile.objects.get(pk=data["lecturer"])

        if not LessonPurchase.objects.filter(student=profile, lesson=lesson).exists():
            raise ValidationError({"lesson": "Lekcja nie została zakupiona."})

        if Review.objects.filter(
            student=profile, lesson=lesson, lecturer=lecturer
        ).exists():
            raise ValidationError({"lesson": "Recenzja już istnieje."})

        return lesson

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        return Review.objects.create(**validated_data, student=profile)
