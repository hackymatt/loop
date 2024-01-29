from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from profile.models import Profile
from django.contrib.auth.models import User


class ProfileVerifySerializer(ModelSerializer):
    email = CharField(source="user.email")
    code = CharField(source="verification_code")

    class Meta:
        model = Profile
        fields = (
            "email",
            "code",
        )
        email = EmailField(required=True)
        code = CharField(write_only=True, required=True)


class ProfileVerificationCodeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
        email = EmailField(required=True)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
