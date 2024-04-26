from core.base_model import BaseModel
from django.db.models import (
    OneToOneField,
    CharField,
    DateField,
    DateTimeField,
    UUIDField,
    ImageField,
    CASCADE,
    Index,
)
from django.contrib.auth.models import User
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / profile / <uuid> / <filename>
    return f"profile/{instance.uuid}/{filename}"  # pragma: no cover


class Profile(BaseModel):
    GENDER_CHOICES = (
        ("M", "Mężczyzna"),
        ("K", "Kobieta"),
        ("I", "Inne"),
    )
    USER_TYPE_CHOICES = (
        ("S", "Student"),
        ("W", "Wykładowca"),
        ("A", "Admin"),
    )
    JOIN_CHOICES = (
        ("Email", "Email"),
        ("Google", "Google"),
        ("Facebook", "Facebook"),
        ("GitHub", "GitHub"),
    )
    uuid = UUIDField(default=uuid.uuid4)
    user = OneToOneField(User, on_delete=CASCADE)
    join_type = CharField(choices=JOIN_CHOICES, default="Email")
    user_type = CharField(choices=USER_TYPE_CHOICES, default="S")
    user_title = CharField(null=True, blank=True)
    verification_code = CharField(max_length=8, null=True)
    verification_code_created_at = DateTimeField(null=True)
    phone_number = CharField(null=True, blank=True)
    dob = DateField(null=True, blank=True)
    gender = CharField(choices=GENDER_CHOICES, default="I", blank=True)
    street_address = CharField(null=True, blank=True)
    zip_code = CharField(null=True, blank=True)
    city = CharField(null=True, blank=True)
    country = CharField(null=True, blank=True)
    image = ImageField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        db_table = "profile"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "user",
                ]
            ),
            Index(
                fields=[
                    "user_type",
                ]
            ),
        ]
