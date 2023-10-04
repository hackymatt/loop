from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from profile.models import Profile
from django.contrib.auth.models import User
from django.core import exceptions


class ProfileDetailsSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")
    gender = CharField(source="get_gender_display")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "dob",
            "gender",
            "street_address",
            "zip_code",
            "city",
            "country",
            "image",
        )

    @staticmethod
    def get(user: User):
        return Profile.objects.get(user_id=user.id)

    @staticmethod
    def model_field_exists(obj, field):
        try:
            obj._meta.get_field(field)
            return True
        except (AttributeError, exceptions.FieldDoesNotExist):
            return False
