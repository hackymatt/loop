from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.password_change.serializers import ProfilePasswordChangeSerializer
from django.contrib.auth.models import User


class ProfilePasswordChangeViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = ProfilePasswordChangeSerializer

    @staticmethod
    def password_change(request):
        data = request.data
        user = request.user
        ProfilePasswordChangeSerializer.validate_data(data)

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"password_change": "Użytkownik niezalogowany."},
            )

        old_password = data["old_password"]
        new_password = data["password"]

        if not user.check_password(old_password):
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"password_change": "Obecne hasło jest nieprawidłowe."},
            )

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK, data={"password_change": "Sukces."})

    def create(self, request, *args, **kwargs):
        return self.password_change(request)
