from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    DecimalField,
    SET,
    PROTECT,
    Index,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from lesson.models import Lesson
from profile.models import Profile


def get_dummy_student_profile():
    user = get_user_model().objects.get(email=settings.DUMMY_STUDENT_EMAIL)
    return Profile.objects.get(user=user)


class Purchase(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=PROTECT)
    student = ForeignKey(
        Profile,
        on_delete=SET(get_dummy_student_profile),
        related_name="lesson_purchase_student",
    )
    price = DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        db_table = "purchase"
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
                    "student",
                    "lesson",
                ]
            ),
        ]
