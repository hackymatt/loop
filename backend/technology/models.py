from core.base_model import BaseModel
from django.db.models import (
    CharField,
    Index,
    QuerySet,
    Manager,
    Subquery,
    OuterRef,
    Value,
    IntegerField,
    Count,
)
from django.db.models.functions import Coalesce
from django.apps import apps


class TechnologyQuerySet(QuerySet):
    def add_courses_count(self):
        Course = apps.get_model("course", "Course")
        total_courses_count = (
            Course.objects.filter(
                active=True, modules__lessons__technologies=OuterRef("pk")
            )
            .annotate(dummy_group_by=Value(1))
            .values("dummy_group_by")
            .order_by("dummy_group_by")
            .annotate(total_courses_count=Count("id", distinct=True))
            .values("total_courses_count")
        )

        return self.annotate(
            courses_count=Coalesce(
                Subquery(total_courses_count), Value(0), output_field=IntegerField()
            )
        )


class TechnologyManager(Manager):
    def get_queryset(self):
        return TechnologyQuerySet(self.model, using=self._db)

    def add_courses_count(self):
        return self.get_queryset().add_courses_count()


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
