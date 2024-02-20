from backend.base_model import BaseModel
from django.db.models import (
    ManyToManyField,
    CharField,
    TextField,
    BooleanField,
    ImageField,
    FileField,
    Index,
)
from lesson.models import Lesson
from topic.models import Topic


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
    level = CharField(choices=LEVEL_CHOICES, null=True)
    skills = ManyToManyField(Skill, related_name="course_skills")
    topics = ManyToManyField(Topic, related_name="course_topics")
    active = BooleanField(default=False)
    image = ImageField(upload_to=course_directory_path)
    video = FileField(upload_to=course_directory_path, null=True, blank=True)
    lessons = ManyToManyField(Lesson, related_name="course_lessons")

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
                    "level",
                ]
            ),
        ]
