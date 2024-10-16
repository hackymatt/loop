from core.base_model import BaseModel
from django.db.models import (
    QuerySet,
    Manager,
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
    Count,
    Avg,
    Subquery,
    Value,
    Prefetch,
    OuterRef,
    FloatField,
)
from django.core.validators import MinValueValidator
from decimal import Decimal
from technology.models import Technology
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce
from django.apps import apps


class LessonQuerySet(QuerySet):
    """Custom QuerySet for Lesson model to add related data."""

    def _add_students_count(self):
        """Annotate the count of students enrolled in each lesson."""
        Purchase = apps.get_model("purchase", "Purchase")
        student_count_subquery = (
            Purchase.objects.filter(lesson=OuterRef("pk"), payment__status="S")
            .values("lesson_id")
            .annotate(total_students=Count("student"))
            .order_by("lesson_id")
            .values("total_students")[:1]  # Limit to 1 for optimization
        )
        return self.annotate(
            students_count=Coalesce(Subquery(student_count_subquery), Value(0))
        )

    def _add_rating(self):
        """Annotate the average rating for each lesson."""
        Review = apps.get_model("review", "Review")

        avg_rating_subquery = (
            Review.objects.filter(lesson=OuterRef("pk"))
            .values("lesson_id")
            .annotate(avg_rating=Avg("rating"))
            .order_by("lesson_id")
            .values("avg_rating")[:1]  # Limit to 1 for optimization
        )
        return self.annotate(
            rating=Coalesce(
                Subquery(avg_rating_subquery), Value(0), output_field=FloatField()
            )
        )

    def _add_rating_count(self):
        """Annotate the total count of ratings for each lesson."""
        Review = apps.get_model("review", "Review")
        rating_count_subquery = (
            Review.objects.filter(lesson=OuterRef("pk"))
            .values("lesson_id")
            .annotate(total_ratings=Count("id"))
            .order_by("lesson_id")
            .values("total_ratings")[:1]  # Limit to 1 for optimization
        )
        return self.annotate(
            rating_count=Coalesce(Subquery(rating_count_subquery), Value(0))
        )

    def _add_technologies(self):
        """Prefetch technologies associated with lessons."""
        Technology = apps.get_model("technology", "Technology")
        return self.prefetch_related(
            Prefetch(
                "technologies",
                queryset=Technology.objects.filter(
                    id__in=self.values_list("technologies__id", flat=True).distinct()
                ),
                to_attr="ordered_technologies",
            )
        )

    def _add_lecturers(self):
        """Annotate the IDs of lecturers associated with each lesson."""
        Teaching = apps.get_model("teaching", "Teaching")
        lecturer_ids_subquery = (
            Teaching.objects.filter(lesson_id=OuterRef("pk"))
            .values("lesson_id")
            .annotate(ids=ArrayAgg("lecturer_id"))
            .values("ids")[:1]  # Limit to 1 for optimization
        )
        return self.annotate(
            lecturers_ids=Coalesce(Subquery(lecturer_ids_subquery), Value([]))
        )

    def add_columns(self):
        """Aggregate all additional columns."""
        return (
            self._add_students_count()
            ._add_rating()
            ._add_rating_count()
            ._add_technologies()
            ._add_lecturers()
        )


class LessonManager(Manager):
    """Custom Manager for Lesson model."""

    def get_queryset(self):
        """Get the customized queryset with additional annotations."""
        return LessonQuerySet(self.model, using=self._db).add_columns()


class Lesson(BaseModel):
    """Lesson model representing educational lessons."""

    title = CharField(max_length=255)  # Added max_length for CharField
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
            Index(fields=["id"]),
        ]


class LessonPriceHistory(BaseModel):
    """Model to track price history of lessons."""

    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "lesson_price_history"
        ordering = ["id"]
        indexes = [
            Index(fields=["id"]),
            Index(fields=["lesson"]),
        ]
