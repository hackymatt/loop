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
    F,
    Sum,
    OuterRef,
    Subquery,
    IntegerField,
    DecimalField,
)
from django.contrib.auth.models import User
from django.db.models.functions import Concat, Coalesce
from django.contrib.postgres.aggregates import ArrayAgg
import uuid
from django.apps import apps


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / profile / <uuid> / <filename>
    return f"profile/{instance.uuid}/{filename}"  # pragma: no cover


class ProfileQuerySet(QuerySet):
    def add_full_name(self):
        return self.annotate(
            full_name=Concat("user__first_name", Value(" "), "user__last_name")
        )

    def add_account(self):
        Finance = apps.get_model("finance", "Finance")
        account_subquery = Finance.objects.filter(
            lecturer__profile=OuterRef("pk")
        ).values("account")[:1]
        return self.annotate(
            account=Case(
                When(user_type="W", then=Subquery(account_subquery)),
                default=Value(None),
                output_field=CharField(),
            )
        )

    def add_rate(self):
        Finance = apps.get_model("finance", "Finance")
        account_subquery = Finance.objects.filter(
            lecturer__profile=OuterRef("pk")
        ).values("rate")[:1]
        return self.annotate(
            rate=Case(
                When(user_type="W", then=Subquery(account_subquery)),
                default=Value(None),
                output_field=CharField(),
            )
        )

    def add_commission(self):
        Finance = apps.get_model("finance", "Finance")
        account_subquery = Finance.objects.filter(
            lecturer__profile=OuterRef("pk")
        ).values("commission")[:1]
        return self.annotate(
            commission=Case(
                When(user_type="W", then=Subquery(account_subquery)),
                default=Value(None),
                output_field=CharField(),
            )
        )


class ProfileManager(Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def add_full_name(self):
        return self.get_queryset().add_full_name()

    def add_account(self):
        return self.get_queryset().add_account()


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
        ("I", "Inny"),
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

    def add_lessons(self):
        return self.annotate(
            lessons=ArrayAgg("teaching_lecturer__lesson__id", distinct=True)
        )

    def add_lessons_duration(self):
        Lesson = apps.get_model("lesson", "Lesson")
        duration = (
            Lesson.objects.filter(teaching_lesson__lecturer=OuterRef("pk"))
            .values("teaching_lesson__lecturer")
            .annotate(total_duration=Sum("duration"))
            .values("total_duration")[:1]
        )
        return self.annotate(
            lessons_duration=Subquery(duration, output_field=IntegerField())
        )

    def add_lessons_price(self):
        Lesson = apps.get_model("lesson", "Lesson")
        prices = (
            Lesson.objects.filter(teaching_lesson__lecturer=OuterRef("pk"))
            .values("teaching_lesson__lecturer")
            .annotate(total_price=Sum("price"))
            .values("total_price")[:1]
        )
        return self.annotate(
            lessons_price=Subquery(prices, output_field=DecimalField())
        )

    def add_lessons_count(self):
        return self.annotate(lessons_count=Count("teaching_lecturer", distinct=True))

    def add_students_count(self):
        Reservation = apps.get_model("reservation", "Reservation")
        students_count_subquery = (
            Reservation.objects.filter(schedule__lecturer=OuterRef("pk"))
            .values("lesson")
            .annotate(count=Count("lesson"))
            .values("count")[:1]
        )
        return self.annotate(
            students_count=Coalesce(
                Subquery(students_count_subquery), Value(0), output_field=IntegerField()
            )
        )

    def add_account(self):
        return self.annotate(account=F("finance_lecturer__account"))

    def add_rate(self):
        return self.annotate(rate=F("finance_lecturer__rate"))

    def add_commission(self):
        return self.annotate(commission=F("finance_lecturer__commission"))


class LecturerProfileManager(Manager):
    def get_queryset(self):
        return LecturerProfileQuerySet(self.model, using=self._db)

    def add_full_name(self):
        return self.get_queryset().add_full_name()

    def add_profile_ready(self):
        return self.get_queryset().add_profile_ready()


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


class OtherProfileQuerySet(QuerySet):
    def add_full_name(self):
        return self.annotate(
            full_name=Concat(
                "profile__user__first_name", Value(" "), "profile__user__last_name"
            )
        )


class OtherProfileManager(Manager):
    def get_queryset(self):
        return OtherProfileQuerySet(self.model, using=self._db)

    def add_full_name(self):
        return self.get_queryset().add_full_name()


class OtherProfile(BaseModel):
    profile = OneToOneField(Profile, on_delete=CASCADE)

    objects = OtherProfileManager()

    class Meta:
        db_table = "other_profile"
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
