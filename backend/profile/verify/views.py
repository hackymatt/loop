from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.verify.serializers import (
    ProfileVerificationCodeSerializer,
    ProfileVerifySerializer,
    UserSerializer,
)
from profile.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from profile.verify.utils import VerificationCode
from mailer.mailer import Mailer


class ProfileVerifyViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = Profile.objects.all()
    serializer_class = ProfileVerifySerializer

    @staticmethod
    def verify(request):
        email = request.data["email"]
        code = request.data["code"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"email": "Użytkownik nie istnieje."},
            )

        user = User.objects.get(email=email)

        if user.is_active:
            return Response(
                status=status.HTTP_304_NOT_MODIFIED,
                data={"email": "Użytkownik już jest aktywny."},
            )

        profile = Profile.objects.get(user=user)
        verification_code = VerificationCode()

        if make_aware(
            datetime.now()
        ) - profile.verification_code_created_at > timedelta(
            seconds=verification_code.timeout()
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"code": "Kod wygasł."},
            )

        if profile.verification_code != code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"code": "Niepoprawny kod."},
            )

        user.is_active = True
        user.save()

        return Response(
            status=status.HTTP_200_OK, data=UserSerializer(instance=user).data
        )

    def create(self, request, *args, **kwargs):
        return self.verify(request)


class ProfileVerificationCodeViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = Profile.objects.all()
    serializer_class = ProfileVerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"email": "Użytkownik nie istnieje."},
            )

        user = User.objects.get(email=email)
        profile = Profile.objects.get(user=user)

        verification_code = VerificationCode()
        code = verification_code.generate()

        profile.verification_code = code
        profile.verification_code_created_at = make_aware(datetime.now())
        profile.save()

        mailer = Mailer()

        data = {
            "email": user.email,
            "valid_for": int(verification_code.timeout() / 3600),
            "code": code,
        }

        mailer.send(
            email_template="verify.html",
            to=[user.email],
            subject="Aktywuj swoje konto.",
            data=data,
        )

        return Response(status=status.HTTP_200_OK, data={})
