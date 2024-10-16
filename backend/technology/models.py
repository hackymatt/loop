from core.base_model import BaseModel
from django.db.models import (
    CharField,
    Index,
    QuerySet,
    Manager,
    Value,
    Subquery,
    Count,
    OuterRef,
)
from django.db.models.functions import Coalesce
from django.apps import apps


class TechnologyQuerySet(QuerySet):
    """Custom QuerySet for Technology model to add related data."""

    def _add_courses_count(self):
        """Annotate the count of courses using technology."""
        Course = apps.get_model("course", "Course")
        course_count_subquery = (
            Course.objects.filter(modules__lessons__technologies=OuterRef("pk"))
            .values("id")
            .annotate(total_courses=Count("id"))
            .values("total_courses")[:1]  # Limit to 1 for optimization
        )
        return self.annotate(
            courses_count=Coalesce(Subquery(course_count_subquery), Value(0))
        )

    def add_columns(self):
        """Aggregate all additional columns."""
        return self._add_courses_count()


class TechnologyManager(Manager):
    """Custom Manager for Technology model."""

    def get_queryset(self):
        """Get the customized queryset with additional annotations."""
        return TechnologyQuerySet(self.model, using=self._db).add_columns()


class Technology(BaseModel):
    name = CharField()

    objects = TechnologyManager()

    class Meta:
        db_table = "technology"
        ordering = ["name"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "name",
                ]
            ),
        ]
