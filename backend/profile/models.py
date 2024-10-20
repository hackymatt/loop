from core.base_model import BaseModel
from django.db.models import (
    OneToOneField,
    CharField,
    DateField,
    DateTimeField,
    UUIDField,
    ImageField,
    URLField,
    TextField,
    CASCADE,
    Index,
    Manager,
    QuerySet,
    Value,
    Case,
    When,
    BooleanField,
    Count,
    Avg,
)
from django.contrib.auth.models import User
from django.db.models.functions import Concat
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / profile / <uuid> / <filename>
    return f"profile/{instance.uuid}/{filename}"  # pragma: no cover


class ProfileQuerySet(QuerySet):
    def add_full_name(self):
        return self.annotate(
            full_name=Concat("user__first_name", Value(" "), "user__last_name")
        )


class ProfileManager(Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def add_full_name(self):
        return self.get_queryset().add_full_name()


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

    objects = ProfileManager()

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


class AdminProfile(BaseModel):
    profile = OneToOneField(Profile, on_delete=CASCADE)

    class Meta:
        db_table = "admin_profile"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "profile",
                ]
            ),
        ]


class StudentProfileQuerySet(QuerySet):
    def add_full_name(self):
        return self.annotate(
            full_name=Concat(
                "profile__user__first_name", Value(" "), "profile__user__last_name"
            )
        )


class StudentProfileManager(Manager):
    def get_queryset(self):
        return StudentProfileQuerySet(self.model, using=self._db)

    def add_full_name(self):
        return self.get_queryset().add_full_name()


class StudentProfile(BaseModel):
    profile = OneToOneField(Profile, on_delete=CASCADE)

    objects = StudentProfileManager()

    class Meta:
        db_table = "student_profile"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "profile",
                ]
            ),
        ]


class LecturerProfileQuerySet(QuerySet):
    def add_full_name(self):
        return self.annotate(
            full_name=Concat(
                "profile__user__first_name", Value(" "), "profile__user__last_name"
            )
        )

    def add_profile_ready(self):
        return self.annotate(
            profile_ready=Case(
                When(title__isnull=False, description__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

    def add_rating_count(self):
        return self.annotate(rating_count=Count("review_lecturer", distinct=True))

    def add_rating(self):
        return self.annotate(rating=Avg("review_lecturer__rating", distinct=True))

    def add_lessons_count(self):
        return self.annotate(lessons_count=Count("teaching_lecturer", distinct=True))


class LecturerProfileManager(Manager):
    def get_queryset(self):
        return LecturerProfileQuerySet(self.model, using=self._db)

    def add_full_name(self):
        return self.get_queryset().add_full_name()

    def add_profile_ready(self):
        return self.get_queryset().add_profile_ready()

    def add_rating_count(self):
        return self.get_queryset().add_rating_count()

    def add_rating(self):
        return self.get_queryset().add_rating()

    def add_lessons_count(self):
        return self.get_queryset().add_lessons_count()


class LecturerProfile(BaseModel):
    profile = OneToOneField(Profile, on_delete=CASCADE)
    title = CharField(null=True, blank=True)
    description = TextField(null=True, blank=True)
    linkedin_url = URLField(null=True, blank=True)

    objects = LecturerProfileManager()

    class Meta:
        db_table = "lecturer_profile"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "profile",
                ]
            ),
        ]
