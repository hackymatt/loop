from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    TextField,
    DecimalField,
    PROTECT,
    SET,
    Index,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from lesson.models import Lesson
from profile.models import Profile, StudentProfile, LecturerProfile
from config_global import DUMMY_STUDENT_EMAIL, DUMMY_LECTURER_EMAIL


def get_dummy_student_profile():
    user = get_user_model().objects.get(email=DUMMY_STUDENT_EMAIL)
    profile = Profile.objects.get(user=user)
    return StudentProfile.objects.get(profile=profile)


def get_dummy_lecturer_profile():
    user = get_user_model().objects.get(email=DUMMY_LECTURER_EMAIL)
    profile = Profile.objects.get(user=user)
    return LecturerProfile.objects.get(profile=profile)


class Review(BaseModel):
    lesson = ForeignKey(
        Lesson,
        on_delete=PROTECT,
        related_name="review_lesson",
    )
    student = ForeignKey(
        StudentProfile,
        on_delete=SET(get_dummy_student_profile),
        related_name="review_student",
    )
    lecturer = ForeignKey(
        LecturerProfile,
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
