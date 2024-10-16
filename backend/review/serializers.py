from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
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
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = StudentProfile
        fields = (
            "first_name",
            "gender",
            "image",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


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
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        if self.context["request"].method == "PUT":
            return lesson

        lecturer = LecturerProfile.objects.get(
            pk=self.context["request"].data["lecturer"]
        )

        # Check if lesson is purchased
        if not Purchase.objects.filter(
            student__profile=profile, lesson=lesson, payment__status="S"
        ).exists():
            raise ValidationError({"lesson": "Lekcja nie została zakupiona."})

        # Check if review already exists
        if Review.objects.filter(
            student__profile=profile, lesson=lesson, lecturer=lecturer
        ).exists():
            raise ValidationError({"lesson": "Recenzja już istnieje."})

        return lesson

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        student_profile = StudentProfile.objects.get(profile=profile)
        review = Review.objects.create(**validated_data, student=student_profile)

        self._send_notification(review)

        return review

    def _send_notification(self, review):
        notify(
            profile=review.lecturer.profile,
            title="Otrzymano nową recenzję",
            subtitle=review.lesson.title,
            description=f"Otrzymano nową recenzję. Ocena {review.rating}.",
            path=f"/account/teacher/reviews/?sort_by=-created_at&page_size=10&lesson_id={review.lesson.id}",
            icon="mdi:star-rate",
        )
