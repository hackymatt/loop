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


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    email = EmailField(source="profile.user.email")
    street_address = CharField(source="profile.street_address")
    zip_code = CharField(source="profile.zip_code")
    city = CharField(source="profile.city")
    country = CharField(source="profile.country")
    account = SerializerMethodField()

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

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name

    def get_account(self, lecturer: LecturerProfile):
        return lecturer.account


class LecturerEarningSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    earnings = FloatField(source="cost")


class EarningByLecturerSerializer(Serializer):
    lecturer = SerializerMethodField()
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    earnings = FloatField(source="cost")

    def get_lecturer(self, obj):
        lecturer = (
            LecturerProfile.objects.add_full_name()
            .add_account()
            .get(id=obj["lecturer"])
        )
        return LecturerSerializer(lecturer).data


class AdminEarningLecturerSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()
