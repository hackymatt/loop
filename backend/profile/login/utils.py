import requests

from typing import Dict, Any
from django.conf import settings
from rest_framework.serializers import ValidationError
from django.core.files.base import ContentFile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

FACEBOOK_ACCESS_TOKEN_OBTAIN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
FACEBOOK_USER_INFO_URL = "https://graph.facebook.com/v19.0/me/"


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Google"}
        )

    access_token = response.json()["access_token"]

    return access_token


def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    params = {"access_token": access_token}
    response = requests.get(GOOGLE_USER_INFO_URL, params=params)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Google"}
        )

    return response.json()


def facebook_get_access_token(*, code: str, redirect_uri: str) -> str:
    params = {
        "code": code,
        "client_id": settings.FACEBOOK_CLIENT_ID,
        "client_secret": settings.FACEBOOK_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.get(FACEBOOK_ACCESS_TOKEN_OBTAIN_URL, params=params)

    if not response.ok:
        raise ValidationError(
            {"root": "1Wystąpił błąd podczas pobierania danych użytkownika od Facebook"}
        )

    access_token = response.json()["access_token"]

    return access_token


def facebook_get_user_info(*, access_token: str) -> Dict[str, Any]:
    params = {
        "access_token": access_token,
        "fields": "email,first_name,last_name,birthday,gender,picture.type(large)",
    }
    response = requests.get(FACEBOOK_USER_INFO_URL, params=params)

    if not response.ok:
        raise ValidationError(
            {"root": "2Wystąpił błąd podczas pobierania danych użytkownika od Google"}
        )

    return response.json()


def get_image_content(url: str) -> str:
    response = requests.get(url)
    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Google"}
        )

    return ContentFile(response.content)
