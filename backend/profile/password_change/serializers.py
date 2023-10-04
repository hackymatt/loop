from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from profile.validators import (
    validate_password_do_not_match,
    validate_password_match,
    validate_password_strength,
)


class ProfilePasswordChangeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "old_password",
            "password",
            "password2",
        )

    old_password = CharField(write_only=True, required=True)
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    @staticmethod
    def validate_data(data):
        validate_password_do_not_match(data["old_password"], data["password"])
        validate_password_strength(data["password"])
        validate_password_match(data["password"], data["password2"])
