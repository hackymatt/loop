from backend.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    DecimalField,
    CASCADE,
    PROTECT,
    Index,
)
from course.models import Course, Lesson
from profile.models import Profile


class CoursePurchase(BaseModel):
    course = ForeignKey(
        Course,
        on_delete=PROTECT,
    )
    student = ForeignKey(
        Profile, on_delete=PROTECT, related_name="course_purchase_student"
    )
    price = DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = "course_purchase"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "student",
                ]
            ),
        ]


class LessonPurchase(BaseModel):
    course_purchase = ForeignKey(CoursePurchase, on_delete=PROTECT)
    lesson = ForeignKey(Lesson, on_delete=PROTECT)
    student = ForeignKey(
        Profile, on_delete=CASCADE, related_name="lesson_purchase_student"
    )
    price = DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = "lesson_purchase"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lesson", "student"],
                name="lesson_purchase_lesson_student_unique_together",
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
                    "student",
                    "lesson",
                ]
            ),
        ]
