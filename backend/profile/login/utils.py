import requests

from typing import Dict, Any
from django.conf import settings
from rest_framework.serializers import ValidationError
from django.core.files.base import ContentFile

from django.contrib.auth.models import User
from profile.models import Profile, StudentProfile, AdminProfile, LecturerProfile
from newsletter.models import Newsletter

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

FACEBOOK_ACCESS_TOKEN_OBTAIN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
FACEBOOK_USER_INFO_URL = "https://graph.facebook.com/v19.0/me/"

GITHUB_ACCESS_TOKEN_OBTAIN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_EMAIL_URL = "https://api.github.com/user/emails"
GITHUB_USER_INFO_URL = "https://api.github.com/user"


def google_get_access_token_request(data):
    return requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)  # pragma: no cover


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = google_get_access_token_request(data=data)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Google"}
        )

    access_token = response.json()["access_token"]

    return access_token


def google_get_user_info_request(params):
    return requests.get(GOOGLE_USER_INFO_URL, params=params)  # pragma: no cover


def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    params = {"access_token": access_token}
    response = google_get_user_info_request(params=params)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Google"}
        )

    return response.json()


def facebook_get_access_token_request(params):
    return requests.get(
        FACEBOOK_ACCESS_TOKEN_OBTAIN_URL, params=params
    )  # pragma: no cover


def facebook_get_access_token(*, code: str, redirect_uri: str) -> str:
    params = {
        "code": code,
        "client_id": settings.FACEBOOK_CLIENT_ID,
        "client_secret": settings.FACEBOOK_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
    }
    response = facebook_get_access_token_request(params=params)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Facebook"}
        )

    access_token = response.json()["access_token"]

    return access_token


def facebook_get_user_info_request(params):
    return requests.get(FACEBOOK_USER_INFO_URL, params=params)  # pragma: no cover


def facebook_get_user_info(*, access_token: str) -> Dict[str, Any]:
    params = {
        "access_token": access_token,
        "fields": "email,first_name,last_name,birthday,gender,picture.type(large)",
    }
    response = facebook_get_user_info_request(params=params)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od Facebook"}
        )

    return response.json()


def github_get_access_token_request(data):
    return requests.post(
        GITHUB_ACCESS_TOKEN_OBTAIN_URL,
        data=data,
        headers={"Accept": "application/json"},
    )  # pragma: no cover


def github_get_access_token(*, code: str, redirect_uri: str) -> str:
    data = {
        "code": code,
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
    }
    response = github_get_access_token_request(data=data)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od GitHub"}
        )
    access_token = response.json()["access_token"]

    return access_token


def github_get_user_email_request(headers):
    return requests.get(GITHUB_USER_EMAIL_URL, headers=headers)  # pragma: no cover


def github_get_user_email(*, access_token: str) -> Dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
    }
    response = github_get_user_email_request(headers=headers)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od GitHub"}
        )

    return response.json()


def github_get_user_info_request(headers):
    return requests.get(GITHUB_USER_INFO_URL, headers=headers)  # pragma: no cover


def github_get_user_info(*, access_token: str) -> Dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
    }
    response = github_get_user_info_request(headers=headers)

    if not response.ok:
        raise ValidationError(
            {"root": "Wystąpił błąd podczas pobierania danych użytkownika od GitHub"}
        )

    return response.json()


def get_image_content_request(url: str):
    return requests.get(url)  # pragma: no cover


def get_image_content(url: str, provider: str) -> str:
    response = get_image_content_request(url=url)
    if not response.ok:
        raise ValidationError(
            {
                "root": f"Wystąpił błąd podczas pobierania danych użytkownika od {provider}"
            }
        )

    return ContentFile(response.content)


def create_user(username, email, first_name, last_name, dob, gender, image, join_type):
    user, _ = User.objects.get_or_create(email=email)
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.is_active = True
    user.save()

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.dob = dob
    profile.gender = gender
    profile.join_type = join_type
    profile.save()

    user_type = profile.user_type
    if user_type[0] == "A":
        AdminProfile.objects.get_or_create(profile=profile)
    elif user_type[0] == "W":
        LecturerProfile.objects.get_or_create(profile=profile)
    else:
        StudentProfile.objects.get_or_create(profile=profile)

    if image:
        profile.image.save(f"{profile.uuid}.jpg", image)

    newsletter, created = Newsletter.objects.get_or_create(email=email)
    if not created:
        newsletter.active = True
        newsletter.save()

    return user, profile
