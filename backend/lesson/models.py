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
    Exists,
    Min,
)
from technology.models import Technology
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.postgres.aggregates import ArrayAgg
from profile.models import Profile
from datetime import datetime, timedelta
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

    def add_previous_price(self):
        latest_price_subquery = (
            LessonPriceHistory.objects.filter(lesson=OuterRef("pk"))
            .order_by("-created_at")
            .values("price")[:1]
        )
        exists_subquery = LessonPriceHistory.objects.filter(lesson=OuterRef("pk"))

        return self.annotate(
            previous_price=Case(
                When(
                    Exists(exists_subquery),
                    then=Case(
                        When(
                            price__gt=Subquery(latest_price_subquery), then=Value(None)
                        ),
                        default=Subquery(latest_price_subquery),
                        output_field=DecimalField(),
                    ),
                ),
                default=None,
                output_field=DecimalField(),
            )
        )

    def add_lowest_30_days_price(self):
        latest_price_subquery = (
            LessonPriceHistory.objects.filter(lesson=OuterRef("pk"))
            .order_by("-created_at")
            .values("price")[:1]
        )
        latest_30_days_price_subquery = (
            LessonPriceHistory.objects.order_by("-created_at")
            .filter(
                lesson=OuterRef("pk"),
                created_at__gte=make_aware(datetime.now() - timedelta(days=30)),
            )
            .values("lesson")
            .order_by("lesson")
            .annotate(min_price=Min("price"))
            .values("min_price")[:1]
        )
        exists_subquery = LessonPriceHistory.objects.filter(lesson=OuterRef("pk"))

        return self.annotate(
            lowest_30_days_price=Case(
                When(
                    Exists(exists_subquery),
                    then=Case(
                        When(
                            price__gt=Subquery(latest_price_subquery), then=Value(None)
                        ),
                        default=Subquery(latest_30_days_price_subquery),
                        output_field=DecimalField(),
                    ),
                ),
                default=None,
                output_field=DecimalField(),
            )
        )

    def add_teaching_id(self, user):
        Teaching = apps.get_model("teaching", "Teaching")
        teaching = Teaching.objects.filter(
            lecturer__profile__user=user, lesson=OuterRef("pk")
        )

        return self.annotate(
            teaching_id=Case(
                When(
                    Exists(teaching),
                    then=Subquery(teaching.values("id")[:1]),
                ),
                default=Value(None),
            )
        )


class LessonManager(Manager):
    def get_queryset(self):
        return LessonQuerySet(self.model, using=self._db)

    def add_lecturers(self):
        return self.get_queryset().add_lecturers()

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
