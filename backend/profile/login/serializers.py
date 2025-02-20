from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    EmailField,
    CharField,
)
from django.contrib.auth.models import User
from profile.models import Profile


class ProfileLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

        email = EmailField(required=True)
        password = CharField(write_only=True, required=True)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ProfileSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "user_type")


class InputSerializer(Serializer):
    code = CharField(required=False)
    error = CharField(required=False)
