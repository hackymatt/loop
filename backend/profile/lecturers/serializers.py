from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    SerializerMethodField,
)
from profile.models import Profile
from purchase.models import LessonPurchase
from review.models import Review
from teaching.models import Teaching
from django.db.models import Avg


def get_rating(lecturer):
    return Review.objects.filter(lecturer=lecturer)

def get_lessons(lecturer):
    return Teaching.objects.filter(lecturer=lecturer).values("lesson")

class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = EmailField(source="get_gender_display")
    email = EmailField(source="user.email")
    rating = SerializerMethodField("get_lecturer_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons_count = SerializerMethodField("get_lecturer_lessons_count")

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
            "rating_count",
            "lessons_count",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name

    def get_lecturer_rating(self, lecturer):
        return get_rating(lecturer=lecturer).aggregate(Avg("rating"))["rating__avg"]
    
    def get_lecturer_rating_count(self, lecturer):
        return get_rating(lecturer=lecturer).count()
    
    def get_lecturer_lessons_count(self, lecturer):
        return (
            get_lessons(lecturer=lecturer)
            .distinct()
            .count()
        )
    

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
