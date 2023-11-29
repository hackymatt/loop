from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from profile.login.serializers import ProfileLoginSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class ProfileLoginViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = ProfileLoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"login": "Niepoprawny email lub hasło."},
            )

        if not User.objects.get(email=email).is_active:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"login": "Użytkownik nieaktywny."},
            )

        password = request.data["password"]
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"login": "Niepoprawny email lub hasło."},
            )

        login(request, user)
        return Response(status=status.HTTP_200_OK, data={"login": "Sukces."})
