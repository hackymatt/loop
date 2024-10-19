from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    CharField,
    TextField,
    BooleanField,
    PositiveIntegerField,
    URLField,
    DecimalField,
    ManyToManyField,
    CASCADE,
    Index,
    QuerySet,
    Manager,
    Count,
    Avg,
    Value,
    OuterRef,
    FloatField,
    Subquery,
    Case,
    When,
    F,
)
from technology.models import Technology
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce
from profile.models import Profile
from datetime import datetime
from django.utils.timezone import make_aware
from django.apps import apps


class LessonQuerySet(QuerySet):
    def add_lecturers(self):
        return self.annotate(
            lecturers_ids=ArrayAgg("teaching_lesson__lecturer__id", distinct=True)
        )

    def add_students_count(self):
        return self.annotate(students_count=Count("purchase_lesson", distinct=True))

    def add_rating(self):
        return self.annotate(rating=Avg("review_lesson__rating", distinct=True))

    def add_rating_count(self):
        return self.annotate(rating_count=Count("review_lesson", distinct=True))

    def add_progress(self, user):
        if not user.is_authenticated:
            return self.annotate(progress=Value(None, output_field=FloatField()))

        profile = Profile.objects.get(user=user)
        if not profile.user_type[0] == "S":
            return self.annotate(progress=Value(None, output_field=FloatField()))

        Reservation = apps.get_model("reservation", "Reservation")
        student_lessons = Reservation.objects.filter(
            student__profile__user=user,
            lesson=OuterRef("pk"),
            schedule__end_time__lte=make_aware(datetime.now()),
        ).values("lesson")

        return self.annotate(progress=Count(student_lessons, distinct=True))


class LessonManager(Manager):
    def get_queryset(self):
        return LessonQuerySet(self.model, using=self._db)

    def add_lecturers(self):
        return self.get_queryset().add_lecturers()

    def add_students_count(self):
        return self.get_queryset().add_students_count()

    def add_rating(self):
        return self.get_queryset().add_rating()

    def add_rating_count(self):
        return self.get_queryset().add_rating_count()

    def add_progress(self, user):
        return self.get_queryset().add_progress(user=user)


class Lesson(BaseModel):
    title = CharField()
    description = TextField()
    technologies = ManyToManyField(Technology, related_name="lesson_technologies")
    duration = PositiveIntegerField()
    github_url = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    active = BooleanField(default=False)

    objects = LessonManager()

    class Meta:
        db_table = "lesson"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]


class LessonPriceHistory(BaseModel):
    lesson = ForeignKey(
        Lesson, on_delete=CASCADE, related_name="lesson_price_history_student"
    )
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "lesson_price_history"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "lesson",
                ]
            ),
        ]
