from rest_framework.serializers import ModelSerializer, EmailField, ValidationError
from django.contrib.auth.models import User


class ProfilePasswordResetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)

    email = EmailField(required=True)
