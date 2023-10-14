from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from profile.models import Profile


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


class LecturerDetailsSerializer(ModelSerializer):
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
            "user_type",
            "user_title",
            "phone_number",
            "dob",
            "gender",
            "street_address",
            "zip_code",
            "city",
            "country",
            "image",
        )
