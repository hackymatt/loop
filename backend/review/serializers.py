from rest_framework.serializers import ModelSerializer, CharField, EmailField
from review.models import Review
from profile.models import Profile


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

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        return Review.objects.create(**validated_data, student=profile)
