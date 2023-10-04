from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.verify.serializers import (
    ProfileVerificationCodeSerializer,
    ProfileVerifySerializer,
)
from profile.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


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
                data={"verify": "Użytkownik nie istnieje."},
            )

        user = User.objects.get(email=email)

        if user.is_active:
            return Response(
                status=status.HTTP_304_NOT_MODIFIED,
                data={"code": "Użytkownik już jest aktywny."},
            )

        profile = Profile.objects.get(user_id=user.id)

        if make_aware(
            datetime.now()
        ) - profile.verification_code_created_at > timedelta(
            seconds=ProfileVerifySerializer.verification_code_timeout()
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"code": "Kod wygasł."}
            )

        if profile.verification_code != code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"code": "Niepoprawny kod."},
            )

        user.is_active = True
        user.save()

        return Response(status=status.HTTP_200_OK, data={"code": "Kod poprawny."})

    def create(self, request, *args, **kwargs):
        return self.verify(request)


class ProfileVerificationCodeViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = Profile.objects.all()
    serializer_class = ProfileVerificationCodeSerializer

    @staticmethod
    def regenerate(request):
        data = request.data
        email = data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"verify": "Użytkownik nie istnieje."},
            )

        user = User.objects.get(email=email)
        profile = Profile.objects.get(user_id=user.id)

        profile.verification_code = ProfileVerificationCodeSerializer.generate()
        profile.verification_code_created_at = make_aware(datetime.now())
        profile.save()

        ProfileVerificationCodeSerializer.send(
            profile, "verification_email.html", "Aktywuj swoje konto."
        )

        return Response(status=status.HTTP_200_OK, data={"code": "Kod wysłany."})

    def create(self, request, *args, **kwargs):
        return self.regenerate(request)
