from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    BooleanField,
    SerializerMethodField,
    ValidationError,
)
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.models import User
from profile.models import (
    Profile,
    LecturerProfile,
    AdminProfile,
    StudentProfile,
    OtherProfile,
)
from finance.models import Finance, FinanceHistory
from notification.utils import notify
from const import UserType


class UserSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")
    active = BooleanField(source="user.is_active", required=False)
    image = Base64ImageField(required=False)
    rate = SerializerMethodField()
    commission = SerializerMethodField()
    account = SerializerMethodField()

    def get_rate(self, profile: Profile):
        return profile.rate

    def get_commission(self, profile: Profile):
        return profile.commission

    def get_account(self, profile: Profile):
        return profile.account

    class Meta:
        model = Profile
        exclude = (
            "uuid",
            "modified_at",
            "verification_code",
            "verification_code_created_at",
            "user",
        )

    def validate_user_type(self, user_type):
        user_types = (
            [UserType.OTHER]
            if self.context["request"].method == "POST"
            else [UserType.ADMIN, UserType.INSTRUCTOR, UserType.STUDENT, UserType.OTHER]
        )
        if not user_type in user_types:
            raise ValidationError("Niepoprawna wartość dla user_type.")

        return user_type

    def validate_email(self, email):
        if self.context["request"].method == "POST":
            if User.objects.filter(email=email).exists():
                raise ValidationError("Użytkownik już istnieje.")

        return email

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create(
            username=user_data["email"],
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            is_active=False,
        )

        new_profile = Profile.objects.create(user=user, **validated_data)

        profile = (
            Profile.objects.add_account()
            .add_rate()
            .add_commission()
            .get(id=new_profile.id)
        )

        OtherProfile.objects.create(profile=profile)

        return profile

    def update(self, instance: Profile, validated_data):
        current_user_type = instance.user_type
        user_type = validated_data.get("user_type")

        if current_user_type[0] != user_type[0]:
            if user_type == UserType.ADMIN:
                AdminProfile.objects.get_or_create(profile=instance)
            elif user_type == UserType.INSTRUCTOR:
                LecturerProfile.objects.get_or_create(profile=instance)
                notify(
                    profile=instance,
                    title="Gratulacje! Jesteś nauczycielem",
                    subtitle="",
                    description="Zostałeś nauczycielem, w celu prowadzenia szkoleń uzupełnij swój profil instruktora.",
                    path="/account/teacher/profile",
                    icon="mdi:teach",
                )
            elif user_type == UserType.STUDENT:
                StudentProfile.objects.get_or_create(profile=instance)
            else:
                OtherProfile.objects.get_or_create(profile=instance)

            if current_user_type == UserType.ADMIN:
                AdminProfile.objects.get(profile=instance).delete()
            elif current_user_type == UserType.INSTRUCTOR:
                LecturerProfile.objects.get(profile=instance).delete()
            elif current_user_type == UserType.STUDENT:
                StudentProfile.objects.get(profile=instance).delete()
            else:
                OtherProfile.objects.get(profile=instance).delete()

        if user_type == UserType.INSTRUCTOR:
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
                notify(
                    profile=instance,
                    title="Stawka została zmieniona",
                    subtitle="",
                    description=f"Twoje wynagrodzenie uległo zmianie. Stawka godzinowa: {rate} zł, prowizja: {commission}%.",
                    path="/account/teacher/finance",
                    icon="mdi:finance",
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

        image = validated_data.pop("image", instance.image)
        instance.image = image
        instance.save()

        Profile.objects.filter(pk=instance.pk).update(**validated_data)
        instance.refresh_from_db()

        return instance
