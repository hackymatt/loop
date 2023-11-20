from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    Index,
)
from course.models import Lesson
from profile.models import Profile


class Wishlist(BaseModel):
    profile = ForeignKey(Profile, on_delete=CASCADE, related_name="wishlist_profile")
    lesson = ForeignKey(Lesson, on_delete=CASCADE)

    class Meta:
        db_table = "wishlist"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["profile", "lesson"],
                name="wishlist_profile_lesson_unique_together",
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
                    "profile",
                ]
            ),
        ]
