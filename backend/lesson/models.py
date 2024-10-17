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
    Subquery,
    Value,
    OuterRef,
    QuerySet,
    Manager,
)
from technology.models import Technology
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce
from django.apps import apps


class LessonQuerySet(QuerySet):
    def add_lecturers(self):
        Teaching = apps.get_model("teaching", "Teaching")
        lecturer_ids_subquery = (
            Teaching.objects.filter(lesson_id=OuterRef("pk"))
            .values("lesson_id")
            .annotate(ids=ArrayAgg("lecturer_id"))
            .values("ids")[:1]
        )
        return self.annotate(
            lecturers_ids=Coalesce(Subquery(lecturer_ids_subquery), Value([]))
        )

    def add_technologies(self):
        lecturer_ids_subquery = (
            Lesson.technologies.through.objects.filter(lesson_id=OuterRef("pk"))
            .values("lesson_id")
            .annotate(ids=ArrayAgg("technology_id"))
            .values("ids")[:1]
        )
        return self.annotate(
            technologies_ids=Coalesce(Subquery(lecturer_ids_subquery), Value([]))
        )


class LessonManager(Manager):
    def get_queryset(self):
        return LessonQuerySet(self.model, using=self._db)

    def add_lecturers(self):
        return self.get_queryset().add_lecturers()

    def add_technologies(self):
        return self.get_queryset().add_technologies()


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
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
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
