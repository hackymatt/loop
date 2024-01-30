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
    full_name = SerializerMethodField("get_full_name")
    gender = EmailField(source="get_gender_display")
    email = EmailField(source="user.email")
    rating = SerializerMethodField("get_lecturer_rating")

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "full_name",
            "gender",
            "email",
            "user_title",
            "image",
            "rating",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name

    def get_lecturer_rating(self, lecturer):
        return get_rating(lecturer=lecturer).aggregate(Avg("rating"))["rating__avg"]


class BestLecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = EmailField(source="get_gender_display")

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "full_name",
            "gender",
            "user_title",
            "image",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name
