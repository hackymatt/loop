from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    TextField,
    DecimalField,
    CASCADE,
    Index,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from course.models import Lesson
from profile.models import Profile


class Review(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    student = ForeignKey(Profile, on_delete=CASCADE, related_name="review_student")
    lecturer = ForeignKey(Profile, on_delete=CASCADE, related_name="review_lecturer")
    rating = DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    review = TextField(null=True)

    class Meta:
        db_table = "review"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "student", "lecturer"],
                name="review_lesson_student_lecturer_unique_together",
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
                    "lesson",
                ]
            ),
            Index(
                fields=[
                    "lecturer",
                ]
            ),
            Index(
                fields=[
                    "rating",
                ]
            ),
            Index(
                fields=[
                    "rating",
                    "review",
                ]
            ),
        ]
