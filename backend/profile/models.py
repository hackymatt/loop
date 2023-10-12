from django.db.models import (
    Model,
    OneToOneField,
    CharField,
    DateField,
    DateTimeField,
    UUIDField,
    ImageField,
    CASCADE,
)
from django.contrib.auth.models import User
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / profile / <uuid>/<filename>
    return "profile/{0}/{1}".format(instance.uuid, filename)


class Profile(Model):
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
    uuid = UUIDField(default=uuid.uuid4)
    user = OneToOneField(User, on_delete=CASCADE)
    user_type = CharField(choices=USER_TYPE_CHOICES, default="S")
    user_title = CharField(null=True)
    verification_code = CharField(max_length=8, null=True)
    verification_code_created_at = DateTimeField(null=True)
    phone_number = CharField(null=True)
    dob = DateField(null=True)
    gender = CharField(choices=GENDER_CHOICES, null=True)
    street_address = CharField(null=True)
    zip_code = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    image = ImageField(upload_to=user_directory_path, blank=True)

    class Meta:
        db_table = "profile"
