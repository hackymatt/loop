from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from profile.models import Profile


class LecturerSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
            "user_title",
            "image",
        )
