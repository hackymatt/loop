from django.db.models import (
    Model,
    UniqueConstraint,
    ForeignKey,
    TextField,
    PositiveIntegerField,
    DateTimeField,
    CASCADE,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from course.models import Lesson
from profile.models import Profile


class Review(Model):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    student = ForeignKey(Profile, on_delete=CASCADE)
    rating = PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = TextField(null=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "student"],
                name="review_lesson_student_unique_together",
            )
        ]
