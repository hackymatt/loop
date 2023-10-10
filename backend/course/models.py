from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    TextField,
    PositiveIntegerField,
    URLField,
    DecimalField,
    CASCADE,
)
from django.core.validators import MinValueValidator
from decimal import Decimal


class Course(Model):
    LEVEL_CHOICES = (
        ("P", "Podstawowy"),
        ("Ś", "Średniozaawansowany"),
        ("Z", "Zaawansowany"),
        ("E", "Ekspert"),
    )
    title = CharField()
    description = TextField()
    technology = CharField()
    level = CharField(choices=LEVEL_CHOICES, null=True)
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    github_repo_link = URLField()

    class Meta:
        db_table = "course"


class Lesson(Model):
    course = ForeignKey(Course, on_delete=CASCADE)
    title = CharField()
    description = TextField()
    duration = PositiveIntegerField()
    github_branch_link = URLField()
    price = DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    class Meta:
        db_table = "lesson"