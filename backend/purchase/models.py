from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    DecimalField,
    UUIDField,
    BigIntegerField,
    IntegerField,
    CharField,
    SET,
    PROTECT,
    Index,
)
from django.contrib.auth import get_user_model
from lesson.models import Lesson
from profile.models import Profile, StudentProfile
from config_global import DUMMY_STUDENT_EMAIL
import uuid


def get_dummy_student_profile():
    user = get_user_model().objects.get(email=DUMMY_STUDENT_EMAIL)
    profile = Profile.objects.get(user=user)
    return StudentProfile.objects.get(profile=profile)


class Payment(BaseModel):
    session_id = UUIDField(default=uuid.uuid4)
    order_id = BigIntegerField(null=True)
    amount = IntegerField()
    status = CharField(null=True, default=None)

    class Meta:
        db_table = "payment"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "session_id",
                ]
            ),
            Index(
                fields=[
                    "order_id",
                ]
            ),
        ]


class Purchase(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=PROTECT)
    student = ForeignKey(
        StudentProfile,
        on_delete=SET(get_dummy_student_profile),
        related_name="lesson_purchase_student",
    )
    price = DecimalField(max_digits=7, decimal_places=2, null=True)
    payment = ForeignKey(Payment, on_delete=PROTECT)

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
