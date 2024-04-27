from rest_framework.serializers import ModelSerializer, Serializer, EmailField, CharField
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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class InputSerializer(Serializer):
    code = CharField(required=False)
    error = CharField(required=False)
