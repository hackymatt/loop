from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from drf_extra_fields.fields import Base64ImageField
from profile.models import Profile


class ProfileDetailsSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")
    gender = CharField(source="get_gender_display", allow_blank=True)
    image = Base64ImageField(required=False)
    user_type = CharField(source="get_user_type_display", required=False)

    class Meta:
        model = Profile
        fields = (
            "uuid",
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
            "user_type",
        )

    def update(self, instance, validated_data):
        user = validated_data.pop("user")
        user.pop("email")
        if "get_user_type_display" in validated_data:
            validated_data.pop("get_user_type_display")

        first_name = user.pop("first_name", instance.user.first_name)
        last_name = user.pop("last_name", instance.user.last_name)
        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.user.save()

        gender = validated_data.pop("get_gender_display", instance.gender)
        image = validated_data.pop("image", instance.image)
        instance.gender = gender
        instance.image = image
        instance.save()

        Profile.objects.filter(pk=instance.pk).update(**validated_data)
        instance = Profile.objects.get(pk=instance.pk)

        return instance
