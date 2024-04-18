from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    IntegerField,
    FloatField,
    BooleanField,
    SerializerMethodField,
    EmailField,
    CharField,
)
from profile.models import Profile
from finance.models import Finance


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="user.email")
    account = SerializerMethodField("get_account")

    class Meta:
        model = Profile
        fields = (
            "email",
            "full_name",
            "street_address",
            "zip_code",
            "city",
            "country",
            "account",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name

    def get_account(self, profile):
        return Finance.objects.get(lecturer=profile).account


class LecturerEarningSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    earnings = FloatField(source="cost")


class EarningByLecturerSerializer(Serializer):
    lecturer = SerializerMethodField("get_lecturer")
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()

    def get_lecturer(self, obj):
        return LecturerSerializer(Profile.objects.get(id=obj["lecturer"])).data


class AdminEarningLecturerSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()
