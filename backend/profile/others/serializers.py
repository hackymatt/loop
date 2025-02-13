from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from profile.models import OtherProfile


class OtherSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = OtherProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, other: OtherProfile):
        return other.full_name
