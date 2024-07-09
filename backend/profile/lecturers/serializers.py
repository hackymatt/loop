from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    UUIDField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from profile.models import LecturerProfile
from review.models import Review
from teaching.models import Teaching
from django.db.models import Avg


def get_rating(lecturer):
    return Review.objects.filter(lecturer=lecturer)


def get_lessons(lecturer):
    return Teaching.objects.filter(lecturer=lecturer).values("lesson")


class LecturerSerializer(ModelSerializer):
    uuid = UUIDField(source="profile.uuid")
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    email = EmailField(source="profile.user.email")
    rating = SerializerMethodField("get_lecturer_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons_count = SerializerMethodField("get_lecturer_lessons_count")
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "uuid",
            "full_name",
            "gender",
            "email",
            "title",
            "image",
            "rating",
            "rating_count",
            "lessons_count",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

    def get_lecturer_rating(self, lecturer):
        return get_rating(lecturer=lecturer).aggregate(Avg("rating"))["rating__avg"]

    def get_lecturer_rating_count(self, lecturer):
        return get_rating(lecturer=lecturer).count()

    def get_lecturer_lessons_count(self, lecturer):
        return get_lessons(lecturer=lecturer).distinct().count()


class BestLecturerSerializer(ModelSerializer):
    uuid = UUIDField(source="profile.uuid")
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "uuid",
            "full_name",
            "gender",
            "title",
            "image",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name
