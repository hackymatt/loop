from django.contrib.auth.models import User
from profile.models import Profile
from datetime import datetime
from django.utils.timezone import make_aware
from PIL import Image
from io import BytesIO


def create_user(
    first_name: str, last_name: str, email: str, password: str, is_active: bool
):
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=email,
        is_active=is_active,
    )

    user.set_password(password)
    user.save()

    return user


def create_profile(
    user: User,
    verification_code: str = "abcdefgh",
    verification_code_created_at: datetime = make_aware(datetime.now()),
):
    return Profile.objects.create(
        user=user,
        verification_code=verification_code,
        verification_code_created_at=verification_code_created_at,
    )


def create_image():
    image_data = BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(image_data, format="png")
    image_data.seek(0)

    return image_data
