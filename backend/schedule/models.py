from django.db.models import (
    Model,
    UniqueConstraint,
    ForeignKey,
    DateTimeField,
    CASCADE,
)
from course.models import Lesson
from profile.models import Profile


class Schedule(Model):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    lecturer = ForeignKey(Profile, on_delete=CASCADE, related_name="schedule_lecturer")
    time = DateTimeField()

    class Meta:
        db_table = "schedule"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "lecturer", "time"],
                name="schedule_lesson_lecturer_time_unique_together",
            )
        ]
