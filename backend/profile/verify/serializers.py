from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
)
from profile.models import Profile
from django.contrib.auth.models import User
import string
import random
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

VERIFICATION_CODE_TIMEOUT = 43200  # 12h
VERIFICATION_CODE_LENGTH = 8
CODE_CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits


class ProfileVerifySerializer(ModelSerializer):
    email = CharField(source="user.email")
    code = CharField(source="verification_code")

    class Meta:
        model = Profile
        fields = (
            "email",
            "code",
        )
        email = EmailField(required=True)
        code = CharField(write_only=True, required=True)

    @staticmethod
    def verification_code_timeout():
        return VERIFICATION_CODE_TIMEOUT


class ProfileVerificationCodeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
        email = EmailField(required=True)

    @staticmethod
    def generate():
        return "".join(random.choices(CODE_CHARACTERS, k=VERIFICATION_CODE_LENGTH))

    @staticmethod
    def send(profile: Profile, email_template: str, mail_subject: str):
        code_parts = {
            f"code_{i + 1}": profile.verification_code[i]
            for i in range(0, len(profile.verification_code))
        }

        data = {
            **{
                "valid_for": int(VERIFICATION_CODE_TIMEOUT / 3600),
            },
            **code_parts,
        }
        message = render_to_string(email_template, data)
        email = EmailMultiAlternatives(
            mail_subject, message, "from_email", to=[profile.user.email]
        )
        email.attach_alternative(message, "text/html")

        return email.send()
