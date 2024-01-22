from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ImageField,
    SerializerMethodField,
    ValidationError,
)
from review.models import Review
from profile.models import Profile
from purchase.models import LessonPurchase


class ProfileSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="user.email")
    gender = CharField(source="get_gender_display")
    image = ImageField()

    class Meta:
        model = Profile
        fields = (
            "full_name",
            "email",
            "gender",
            "image",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


class BestReviewSerializer(ModelSerializer):
    student = ProfileSerializer()

    class Meta:
        model = Review
        exclude = (
            "rating",
            "created_at",
            "modified_at",
            "lecturer",
            "lesson",
        )


class ReviewGetSerializer(ModelSerializer):
    lesson_title = CharField(source="lesson.title")
    student = ProfileSerializer()
    lecturer = ProfileSerializer()

    class Meta:
        model = Review
        fields = (
            "id",
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
