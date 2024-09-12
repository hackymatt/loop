from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    EmailField,
    ImageField,
    SerializerMethodField,
    ValidationError,
)
from review.models import Review
from profile.models import Profile, LecturerProfile, StudentProfile
from purchase.models import Purchase
from notification.utils import notify


class StudentSerializer(ModelSerializer):
    first_name = CharField(source="profile.user.first_name")
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = StudentProfile
        fields = (
            "first_name",
            "email",
            "gender",
            "image",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "full_name",
            "email",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


class BestReviewSerializer(ModelSerializer):
    student = StudentSerializer()

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
    student = StudentSerializer()
    lecturer = LecturerSerializer()

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


class ReviewStatsSerializer(ModelSerializer):
    count = IntegerField()

    class Meta:
        model = Review
        fields = (
            "rating",
            "count",
        )


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = ("student",)

    def validate_rating(self, rating):
        if not (rating * 10) % 5 == 0:
            raise ValidationError(
                {"rating": "Ocena musi być całkowita lub połowiczna."}
            )

        return rating

    def validate_lesson(self, lesson):
        request_type = self.context["request"].method

        if request_type == "PUT":
            return lesson

        user = self.context["request"].user
        data = self.context["request"].data
        profile = Profile.objects.get(user=user)
        lecturer = LecturerProfile.objects.get(pk=data["lecturer"])

        if not Purchase.objects.filter(
            student__profile=profile, lesson=lesson
        ).exists():
            raise ValidationError({"lesson": "Lekcja nie została zakupiona."})

        if Review.objects.filter(
            student__profile=profile, lesson=lesson, lecturer=lecturer
        ).exists():
            raise ValidationError({"lesson": "Recenzja już istnieje."})

        return lesson

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        review = Review.objects.create(
            **validated_data, student=StudentProfile.objects.get(profile=profile)
        )

        notify(
            profile=review.lecturer.profile,
            title="Otrzymano nową recenzję",
            subtitle=review.lesson.title,
            description=f"Otrzymano nową recenzję. Ocena {review.rating}, komentarz: {review.review}.",
            path=f"/account/teacher/reviews/?sort_by=-created_at&page_size=10&lesson_id={review.lesson.id}",
            icon="mdi:star-rate",
        )

        return review
