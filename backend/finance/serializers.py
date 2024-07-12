from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from finance.models import Finance, FinanceHistory
from profile.models import LecturerProfile


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "email",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


class FinanceSerializer(ModelSerializer):
    class Meta:
        model = Finance
        exclude = (
            "id",
            "modified_at",
            "created_at",
            "lecturer",
        )

    def update(self, instance, validated_data):
        validated_data.pop("rate")
        validated_data.pop("commission")
        account = validated_data.pop("account")
        current_account = instance.account

        if current_account != account:
            FinanceHistory.objects.create(
                lecturer=instance.lecturer,
                account=current_account,
                rate=instance.rate,
                commission=instance.commission,
            )

        instance.account = account
        instance.save()

        return instance


class FinanceHistorySerializer(ModelSerializer):
    lecturer = LecturerSerializer()

    class Meta:
        model = FinanceHistory
        exclude = ("modified_at",)
