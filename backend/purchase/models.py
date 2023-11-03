from django.db.models import (
    Model,
    UniqueConstraint,
    ForeignKey,
    DateTimeField,
    CASCADE,
)
from course.models import Lesson
from profile.models import Profile


class Purchase(Model):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    profile = ForeignKey(Profile, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "purchase"
        constraints = [
            UniqueConstraint(
                fields=["lesson", "profile"],
                name="purchase_lesson_profile_unique_together",
            )
        ]
