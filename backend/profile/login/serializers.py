from rest_framework.serializers import ModelSerializer, Serializer, CharField
from django.contrib.auth.models import User


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
