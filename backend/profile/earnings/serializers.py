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
from profile.models import LecturerProfile
from finance.models import Finance


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="profile.user.email")
    street_address = CharField(source="profile.street_address")
    zip_code = CharField(source="profile.zip_code")
    city = CharField(source="profile.city")
    country = CharField(source="profile.country")
    account = SerializerMethodField("get_account")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "email",
            "full_name",
            "street_address",
            "zip_code",
            "city",
            "country",
            "account",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

    def get_account(self, lecturer):
        return Finance.objects.get(lecturer=lecturer).account


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
    earnings = FloatField(source="cost")

    def get_lecturer(self, obj):
        return LecturerSerializer(LecturerProfile.objects.get(id=obj["lecturer"])).data


class AdminEarningLecturerSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()
