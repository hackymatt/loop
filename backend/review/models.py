from backend.base_model import BaseModel
from django.db.models import (
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
    review = TextField(null=True, blank=True)

    class Meta:
        db_table = "review"
        ordering = ["id"]
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
