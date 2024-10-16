from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    TextField,
    DecimalField,
    PROTECT,
    SET,
    Index,
    QuerySet,
    Manager,
    Count,
    OuterRef,
    Subquery,
    Value,
)
from django.db.models.functions import Coalesce
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from course.models import Course
from module.models import Module
from lesson.models import Lesson
from profile.models import Profile, StudentProfile, LecturerProfile
from config_global import DUMMY_STUDENT_EMAIL, DUMMY_LECTURER_EMAIL
from django.apps import apps


def get_dummy_student_profile():
    user = get_user_model().objects.get(email=DUMMY_STUDENT_EMAIL)
    profile = Profile.objects.get(user=user)
    return StudentProfile.objects.get(profile=profile)


def get_dummy_lecturer_profile():
    user = get_user_model().objects.get(email=DUMMY_LECTURER_EMAIL)
    profile = Profile.objects.get(user=user)
    return LecturerProfile.objects.get(profile=profile)


class ReviewQuerySet(QuerySet):
    """Custom QuerySet for Review model to add related data."""

    def _add_count(self):
        """Annotate the total count of ratings for each review."""
        return self.annotate(count=Count("rating")).order_by("rating")

    def _add_courses(self):
        """Annotate the IDs of courses associated with each review."""
        module_ids_subquery = Module.lessons.through.objects.filter(
            lesson_id=OuterRef(OuterRef("lesson_id"))
        ).values("module_id")

        course_ids_subquery = (
            Course.modules.through.objects.filter(
                module_id__in=Subquery(module_ids_subquery)
            )
            .values("course_id")
            .annotate(ids=ArrayAgg("course_id"))
            .values("ids")[:1]
        )

        return self.annotate(
            course_ids=Coalesce(Subquery(course_ids_subquery), Value([]))
        )

    def add_columns(self):
        """Aggregate all additional columns."""
        return self._add_count()._add_courses()


class ReviewManager(Manager):
    """Custom Manager for Review model."""

    def get_queryset(self):
        """Get the customized queryset with additional annotations."""
        return ReviewQuerySet(self.model, using=self._db).add_columns()


class Review(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=PROTECT)
    student = ForeignKey(
        StudentProfile,
        on_delete=SET(get_dummy_student_profile),
        related_name="review_student",
    )
    lecturer = ForeignKey(
        LecturerProfile,
        on_delete=SET(get_dummy_lecturer_profile),
        related_name="review_lecturer",
    )
    rating = DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    review = TextField(null=True, blank=True)

    objects = ReviewManager()

    class Meta:
        db_table = "review"
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
            Index(
                fields=[
                    "lecturer",
                ]
            ),
            Index(
                fields=[
                    "rating",
                ]
            ),
            Index(
                fields=[
                    "rating",
                    "review",
                ]
            ),
        ]
