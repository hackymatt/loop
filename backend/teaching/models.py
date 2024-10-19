from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    Index,
    QuerySet,
    Manager,
    Exists,
    OuterRef,
    Case,
    When,
    Value,
)
from lesson.models import Lesson
from profile.models import LecturerProfile


class TeachingQuerySet(QuerySet):
    def add_is_teaching(self, user):
        user = self.request.user
        teaching = Teaching.objects.filter(
            lecturer__profile__user=user, lesson=OuterRef("pk")
        )

        return self.annotate(
            is_teaching=Case(
                When(
                    teaching_exists=Exists(teaching),
                    then=Value(True),
                ),
                default=Value(False),
            )
        )


class TeachingManager(Manager):
    def get_queryset(self):
        return TeachingQuerySet(self.model, using=self._db)

    def add_progress(self, user):
        return self.get_queryset().add_is_teaching(user=user)


class Teaching(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE, related_name="teaching_lesson")
    lecturer = ForeignKey(
        LecturerProfile, on_delete=CASCADE, related_name="teaching_lecturer"
    )

    objects = TeachingManager()

    class Meta:
        db_table = "teaching"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "lecturer"],
                name="teaching_lesson_lecturer_unique_together",
            )
        ]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                    "lesson",
                ]
            ),
        ]
