from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    TextField,
    DecimalField,
    CASCADE,
    SET,
    Index,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from course.models import Lesson
from profile.models import Profile


def get_dummy_student_profile():
    user = get_user_model().objects.get(email=settings.DUMMY_STUDENT_EMAIL)
    return Profile.objects.get(user=user)


def get_dummy_lecturer_profile():
    user = get_user_model().objects.get(email=settings.DUMMY_LECTURER_EMAIL)
    return Profile.objects.get(user=user)


class Review(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    student = ForeignKey(
        Profile, on_delete=SET(get_dummy_student_profile), related_name="review_student"
    )
    lecturer = ForeignKey(
        Profile,
        on_delete=SET(get_dummy_lecturer_profile),
        related_name="review_lecturer",
    )
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
