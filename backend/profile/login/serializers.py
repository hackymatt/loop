from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from django.contrib.auth.models import User


class ProfileLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

        email = EmailField(required=True)
        password = CharField(write_only=True, required=True)
