from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    SerializerMethodField,
)
from profile.models import Profile
from review.models import Review
from teaching.models import Teaching
from django.db.models import Avg


def get_rating(lecturer):
    return Review.objects.filter(lecturer=lecturer)


class LecturerSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")
    rating = SerializerMethodField("get_lecturer_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons_count = SerializerMethodField("get_lessons_count")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
            "user_title",
            "image",
            "rating",
            "rating_count",
            "lessons_count",
        )

    def get_lecturer_rating(self, lecturer):
        return get_rating(lecturer=lecturer).aggregate(Avg("rating"))["rating__avg"]

    def get_lecturer_rating_count(self, lecturer):
        return get_rating(lecturer=lecturer).count()

    def get_lessons_count(self, lecturer):
        return (
            Teaching.objects.filter(lecturer=lecturer)
            .values("lesson")
            .distinct()
            .count()
        )


class BestLecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = EmailField(source="get_gender_display")

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "gender",
            "user_title",
            "image",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name
