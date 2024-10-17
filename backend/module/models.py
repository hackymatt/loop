from core.base_model import BaseModel
from django.db.models import (
    CharField,
    ManyToManyField,
    Index,
)
from lesson.models import Lesson


class Module(BaseModel):
    title = CharField()
    lessons = ManyToManyField(Lesson, related_name="module_lessons")

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
