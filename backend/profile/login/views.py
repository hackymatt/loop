from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.login.serializers import UserSerializer, InputSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings

from profile.login.utils import (
    google_get_access_token,
    google_get_user_info,
    facebook_get_access_token,
    facebook_get_user_info,
    github_get_access_token,
    github_get_user_email,
    github_get_user_info,
    create_user,
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
                data={"root": "Błąd uwierzytelniania"},
            )

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/login/?type=google"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        email = user_data["email"]
        first_name = user_data.get("given_name", "")
        last_name = user_data.get("family_name", "")
        image_url = user_data.get("picture", "")

        if image_url != "":
            image = get_image_content(url=image_url, provider="Google")
        else:
            image = None

        user = create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            dob=None,
            gender="I",
            image=image,
            join_type="Google",
        )

        login(request, user)
        return Response(
            status=status.HTTP_200_OK, data=UserSerializer(instance=user).data
        )


class FacebookLoginViewSet(ModelViewSet):
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
                data={"root": "Błąd uwierzytelniania"},
            )

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/login/?type=facebook"
        access_token = facebook_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = facebook_get_user_info(access_token=access_token)

        email = user_data["email"]
        first_name = user_data.get("first_name", "")
        last_name = user_data.get("last_name", "")
        dob = user_data.get("birthday", None)
        gender = user_data.get("gender", "I")
        image_data = user_data.get("picture", "")

        if dob:
            month, day, year = dob.split("/")
            dob = "-".join([year, month, day])

        if gender == "male":
            gender = "M"
        elif gender == "female":
            gender = "K"
        else:
            gender = "I"

        if image_data != "":
            image_url = image_data["data"]["url"]
            image = get_image_content(url=image_url, provider="Facebook")
        else:
            image = None

        user = create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            image=image,
            join_type="Facebook",
        )

        login(request, user)
        return Response(
            status=status.HTTP_200_OK, data=UserSerializer(instance=user).data
        )


class GithubLoginViewSet(ModelViewSet):
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
                data={"root": "Błąd uwierzytelniania"},
            )

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/login/?type=github"
        access_token = github_get_access_token(code=code, redirect_uri=redirect_uri)

        user_emails = github_get_user_email(access_token=access_token)
        user_data = github_get_user_info(access_token=access_token)

        email = [email["email"] for email in user_emails if email["primary"] == True][0]
        username = user_data["login"]
        image_url = user_data.get("avatar_url", "")

        if image_url != "":
            image = get_image_content(url=image_url, provider="GitHub")
        else:
            image = None

        user = create_user(
            username=email,
            email=email,
            first_name=username,
            last_name=username,
            dob=None,
            gender="I",
            image=image,
            join_type="Github",
        )

        login(request, user)
        return Response(
            status=status.HTTP_200_OK, data=UserSerializer(instance=user).data
        )
