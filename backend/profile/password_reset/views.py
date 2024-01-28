from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.password_reset.serializers import ProfilePasswordResetSerializer
from django.contrib.auth.models import User
from profile.models import Profile
from datetime import datetime
from django.utils.timezone import make_aware
from profile.verify.utils import VerificationCode
from mailer.mailer import Mailer


class ProfilePasswordResetViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = ProfilePasswordResetSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"email": email, "password_reset": "Użytkownik nie istnieje."},
            )

        user = User.objects.get(email=email)

        verification_code = VerificationCode()
        code = verification_code.generate()
        user.set_password(code)
        user.save()

        profile = Profile.objects.get(user=user)
        profile.verification_code = code
        profile.verification_code_created_at = make_aware(datetime.now())
        profile.save()

        mailer = Mailer()

        code_parts = {f"code_{i + 1}": code[i] for i in range(0, len(code))}

        data = {
            **{
                "valid_for": int(verification_code.timeout() / 3600),
            },
            **code_parts,
        }

        mailer.send(
            email_template="password_reset_email.html",
            to=[user.email],
            subject="Twoje tymczasowe hasło.",
            data=data,
        )

        return Response(
            status=status.HTTP_200_OK,
            data={"email": email, "password_reset": "Hasło zresetowane."},
        )
