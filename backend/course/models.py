from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    ManyToManyField,
    CharField,
    TextField,
    PositiveIntegerField,
    URLField,
    DecimalField,
    BooleanField,
    ImageField,
    FileField,
    CASCADE,
    Index,
)
from django.core.validators import MinValueValidator
from decimal import Decimal


class Technology(BaseModel):
    name = CharField()

    class Meta:
        db_table = "technology"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "name",
                ]
            ),
        ]


class Skill(BaseModel):
    name = CharField()

    class Meta:
        db_table = "skill"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "name",
                ]
            ),
        ]


class Topic(BaseModel):
    name = TextField()

    class Meta:
        db_table = "topic"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "name",
                ]
            ),
        ]


def course_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / courses / <filename>
    return f"courses/{filename}"  # pragma: no cover


class Course(BaseModel):
    LEVEL_CHOICES = (
        ("P", "Podstawowy"),
        ("Ś", "Średniozaawansowany"),
        ("Z", "Zaawansowany"),
        ("E", "Ekspert"),
    )
    title = CharField()
    description = TextField()
    technology = ForeignKey(Technology, on_delete=CASCADE, related_name="technology")
    level = CharField(choices=LEVEL_CHOICES, null=True)
    github_url = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    skills = ManyToManyField(Skill, related_name="course_skills")
    topics = ManyToManyField(Topic, related_name="course_topics")
    active = BooleanField(default=False)
    image = ImageField(upload_to=course_directory_path)
    video = FileField(upload_to=course_directory_path, null=True, blank=True)

    class Meta:
        db_table = "course"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "technology",
                ]
            ),
            Index(
                fields=[
                    "level",
                ]
            ),
            Index(
                fields=[
                    "price",
                ]
            ),
            Index(
                fields=[
                    "technology",
                    "level",
                    "price",
                ]
            ),
            Index(
                fields=[
                    "technology",
                    "level",
                ]
            ),
            Index(
                fields=[
                    "technology",
                    "price",
                ]
            ),
            Index(
                fields=[
                    "level",
                    "price",
                ]
            ),
        ]


class Lesson(BaseModel):
    course = ForeignKey(Course, on_delete=CASCADE, related_name="lessons")
    title = CharField()
    description = TextField()
    duration = PositiveIntegerField()
    github_url = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    active = BooleanField(default=False)

    class Meta:
        db_table = "lesson"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "course",
                ]
            ),
        ]


class CoursePriceHistory(BaseModel):
    course = ForeignKey(Course, on_delete=CASCADE)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "course_price_history"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "course",
                ]
            ),
        ]


class LessonPriceHistory(BaseModel):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "lesson_price_history"
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
        ]
