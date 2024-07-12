from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError,
)
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from profile.models import Profile, StudentProfile
from newsletter.models import Newsletter
from datetime import datetime
from django.utils.timezone import make_aware
from profile.validators import validate_password_match, validate_password_strength
from profile.verify.utils import VerificationCode
from mailer.mailer import Mailer


class ProfileRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(required=True)
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("Konto z podanym adresem mailowym już istnieje.")

        return email

    def validate(self, data):
        validate_password_strength(data["password"])
        validate_password_match(data["password"], data["password2"])

        return data

    def create(self, validated_data):
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        password = validated_data["password"]

        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
        )

        user.set_password(password)
        user.save()

        verification_code = VerificationCode()
        code = verification_code.generate()

        profile = Profile.objects.create(
            user=user,
            verification_code=code,
            verification_code_created_at=make_aware(datetime.now()),
        )

        StudentProfile.objects.create(profile=profile)

        mailer = Mailer()

        data = {
            "email": user.email,
            "valid_for": int(verification_code.timeout() / 3600),
            "code": code,
        }

        mailer.send(
            email_template="verify.html",
            to=[user.email],
            subject="Zweryfikuj swoje konto",
            data=data,
        )

        newsletter, created = Newsletter.objects.get_or_create(email=email)
        if not created:
            newsletter.active = True
            newsletter.save()

        return user
