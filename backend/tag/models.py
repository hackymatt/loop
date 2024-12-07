from core.base_model import BaseModel
from django.db.models import TextField, Index, QuerySet, Manager, Count, F, Value
from django.db.models.functions import Coalesce


class TagQuerySet(QuerySet):
    def add_post_count(self):
        return self.annotate(
            post_count=Coalesce(Count("post_tags", distinct=True), Value(0))
        )

    def add_course_count(self):
        return self.annotate(
            course_count=Coalesce(Count("course_tags", distinct=True), Value(0))
        )


class TagManager(Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def add_post_count(self):
        return self.get_queryset().add_post_count()


class Tag(BaseModel):
    name = TextField()

    objects = TagManager()

    class Meta:
        db_table = "tags"
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
