from core.base_model import BaseModel
from django.db.models import (
    CharField,
    ManyToManyField,
    Index,
    QuerySet,
    Manager,
    Prefetch,
    Count,
)
from lesson.models import Lesson


class ModuleQuerySet(QuerySet):
    """Custom QuerySet for Lesson model to add related data."""

    def _add_lessons(self):
        """Prefetch lessons associated with module."""
        return self.prefetch_related(
            Prefetch(
                "lessons",
                queryset=Lesson.objects.filter(
                    id__in=self.values_list("lessons__id", flat=True).distinct()
                ),
                to_attr="ordered_lessons",
            )
        )

    def _add_lessons_count(self):
        """Annotate the number of lessons for each module."""
        return self.annotate(lessons_count=Count("lessons"))

    def add_columns(self):
        """Aggregate all additional columns."""
        return self._add_lessons()._add_lessons_count()


class ModuleManager(Manager):
    """Custom Manager for Module model."""

    def get_queryset(self):
        """Get the customized queryset with additional annotations."""
        return ModuleQuerySet(self.model, using=self._db).add_columns()


class Module(BaseModel):
    """Module model representing a collection of lessons."""

    title = CharField()
    lessons = ManyToManyField(Lesson, related_name="module_lessons")

    objects = ModuleManager()

    class Meta:
        db_table = "module"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]
