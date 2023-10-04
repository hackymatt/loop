from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.password_reset.serializers import ProfilePasswordResetSerializer
from django.contrib.auth.models import User
from profile.models import Profile
from profile.verify.serializers import ProfileVerificationCodeSerializer
from datetime import datetime
from django.utils.timezone import make_aware


class ProfilePasswordResetViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = ProfilePasswordResetSerializer

    @staticmethod
    def password_reset(request):
        data = request.data
        email = data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"password_reset": "Użytkownik nie istnieje."},
            )

        user = User.objects.get(email=email)

        code = ProfileVerificationCodeSerializer.generate()
        user.set_password(code)
        user.save()

        profile = Profile.objects.get(user_id=user.id)
        profile.verification_code = code
        profile.verification_code_created_at = make_aware(datetime.now())
        profile.save()

        ProfileVerificationCodeSerializer.send(
            profile, "password_reset_email.html", "Twoje tymczasowe hasło."
        )

        return Response(
            status=status.HTTP_200_OK, data={"password_reset": "Hasło zresetowane."}
        )

    def create(self, request, *args, **kwargs):
        return self.password_reset(request)
