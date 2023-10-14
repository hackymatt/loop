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
    CASCADE,
)
from django.core.validators import MinValueValidator
from decimal import Decimal
from profile.models import Profile


class Technology(Model):
    name = CharField()

    class Meta:
        db_table = "technology"


class Skill(Model):
    name = CharField()

    class Meta:
        db_table = "skill"


class Topic(Model):
    name = TextField()

    class Meta:
        db_table = "topic"


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


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE, related_name="lessons")
    title = CharField()
    description = TextField()
    duration = PositiveIntegerField()
    github_branch_link = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    lecturers = ManyToManyField(Profile, related_name="lesson_lecturers")

    class Meta:
        db_table = "lesson"
