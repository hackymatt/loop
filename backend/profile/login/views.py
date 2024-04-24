from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.login.serializers import UserSerializer, InputSerializer
from profile.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings

from profile.login.utils import (
    google_get_access_token,
    google_get_user_info,
    get_image_content,
)


class EmailLoginViewSet(ModelViewSet):
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        email = request.data["email"]

        if not User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"root": "Niepoprawny email lub hasło."},
            )

        if not User.objects.get(email=email).is_active:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"root": "Użytkownik nieaktywny.", "email": email},
            )

        password = request.data["password"]
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"root": "Niepoprawny email lub hasło."},
            )

        login(request, user)
        return Response(
            status=status.HTTP_200_OK, data=UserSerializer(instance=user).data
        )


class GoogleLoginViewSet(ModelViewSet):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        input_serializer = InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")

        if error or not code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"root": error},
            )

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/login/?type=google"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            username = user_data["email"]
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")
            image_url = user_data.get("picture", "")
            if image_url != "":
                image = get_image_content(url=image_url)

            user = User.objects.create(
                username=username,
                email=user_data["email"],
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )

            profile = Profile.objects.create(user=user, join_type="Google")
            profile.image.save(f"{profile.uuid}.jpg", image)

        login(request, user)
        return Response(
            status=status.HTTP_200_OK, data=UserSerializer(instance=user).data
        )
