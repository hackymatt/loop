from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from profile.models import Profile, LecturerProfile, AdminProfile, StudentProfile
from finance.models import Finance, FinanceHistory


def get_finance(profile):
    if profile.user_type[0] != "W":
        return None

    finance = Finance.objects.filter(lecturer__profile=profile)

    if not finance.exists():
        return None

    return finance.first()


class FinanceSerializer(ModelSerializer):
    class Meta:
        model = Finance
        fields = ("account",)


class UserSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")
    gender = CharField(source="get_gender_display", allow_blank=True)
    user_type = CharField(source="get_user_type_display", allow_blank=True)
    image = Base64ImageField(required=False)
    rate = SerializerMethodField("get_rate")
    commission = SerializerMethodField("get_commission")
    account = SerializerMethodField("get_account")

    def get_rate(self, profile):
        finance = get_finance(profile=profile)
        if not finance:
            return None
        return finance.rate

    def get_commission(self, profile):
        finance = get_finance(profile=profile)
        if not finance:
            return None
        return finance.commission

    def get_account(self, profile):
        finance = get_finance(profile=profile)
        if not finance:
            return None
        return finance.account

    class Meta:
        model = Profile
        exclude = (
            "modified_at",
            "verification_code",
            "verification_code_created_at",
            "user",
        )

    def update(self, instance, validated_data):
        current_user_type = instance.user_type
        user_type = validated_data.get("get_user_type_display")

        if current_user_type[0] != user_type[0]:
            if user_type[0] == "A":
                AdminProfile.objects.get_or_create(profile=instance)
            elif user_type[0] == "W":
                LecturerProfile.objects.get_or_create(profile=instance)
            else:
                StudentProfile.objects.get_or_create(profile=instance)

            if current_user_type[0] == "A":
                AdminProfile.objects.get(profile=instance).delete()
            elif current_user_type[0] == "W":
                LecturerProfile.objects.get(profile=instance).delete()
            else:
                StudentProfile.objects.get(profile=instance).delete()

        if user_type[0] == "W":
            data = self.context["request"].data
            rate = data["rate"]
            commission = data["commission"]
            finance, _ = Finance.objects.get_or_create(
                lecturer=LecturerProfile.objects.get(profile=instance)
            )
            current_rate = finance.rate
            current_commission = finance.commission

            if current_rate != rate or current_commission != commission:
                FinanceHistory.objects.create(
                    lecturer=LecturerProfile.objects.get(profile=instance),
                    account=finance.account,
                    rate=current_rate,
                    commission=current_commission,
                )

            finance.rate = rate
            finance.commission = commission
            finance.save()

        user = validated_data.pop("user")
        user.pop("email")
        first_name = user.pop("first_name", instance.user.first_name)
        last_name = user.pop("last_name", instance.user.last_name)
        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.user.save()

        gender = validated_data.pop("get_gender_display", instance.gender)
        image = validated_data.pop("image", instance.image)
        user_type = validated_data.pop("get_user_type_display", instance.user_type)
        instance.gender = gender
        instance.image = image
        instance.user_type = user_type
        instance.save()

        Profile.objects.filter(pk=instance.pk).update(**validated_data)
        instance = Profile.objects.get(pk=instance.pk)

        return instance
