from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class ProfileLogoutSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
