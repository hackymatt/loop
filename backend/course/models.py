from django.db.models import (
    Model,
    ForeignKey,
    ManyToManyField,
    CharField,
    TextField,
    PositiveIntegerField,
    URLField,
    DecimalField,
    BooleanField,
    DateTimeField,
    CASCADE,
    Index,
)
from django.core.validators import MinValueValidator
from decimal import Decimal
from profile.models import Profile


class Technology(Model):
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


class Skill(Model):
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


class Topic(Model):
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


class Course(Model):
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
    github_repo_link = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    skills = ManyToManyField(Skill, related_name="course_skills")
    topics = ManyToManyField(Topic, related_name="course_topics")
    active = BooleanField(default=True)

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


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE, related_name="lessons")
    title = CharField()
    description = TextField()
    duration = PositiveIntegerField()
    github_branch_link = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

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


class CoursePriceHistory(Model):
    course = ForeignKey(Course, on_delete=CASCADE)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = DateTimeField(auto_now_add=True)

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


class LessonPriceHistory(Model):
    lesson = ForeignKey(Lesson, on_delete=CASCADE)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = DateTimeField(auto_now_add=True)

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
