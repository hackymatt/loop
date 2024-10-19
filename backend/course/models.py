from core.base_model import BaseModel
from django.db.models import (
    ManyToManyField,
    CharField,
    TextField,
    BooleanField,
    ImageField,
    FileField,
    Index,
    QuerySet,
    Manager,
    Sum,
    Count,
    Value,
    Avg,
    OuterRef,
    FloatField,
    Subquery,
    F,
    DecimalField,
)
from module.models import Module
from skill.models import Skill
from topic.models import Topic
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce, Cast
from datetime import datetime
from django.utils.timezone import make_aware
from reservation.models import Reservation
from profile.models import Profile
from lesson.models import Lesson


def course_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / courses / <filename>
    return f"courses/{filename}"  # pragma: no cover


class CourseQuerySet(QuerySet):
    def add_price(self):
        return self.annotate(price=Sum("modules__lessons__price", distinct=True))

    def add_duration(self):
        return self.annotate(duration=Sum("modules__lessons__duration", distinct=True))

    def add_modules(self):
        return self.annotate(modules=Coalesce(ArrayAgg("modules__id"), Value([])))

    def add_lessons(self):
        return self.annotate(
            lessons=Coalesce(ArrayAgg("modules__lessons__id", distinct=True), Value([]))
        )

    def add_students_count(self):
        return self.annotate(
            students_count=Count("modules__lessons__purchase_lesson", distinct=True)
        )

    def add_rating_count(self):
        return self.annotate(
            rating_count=Count("modules__lessons__review_lesson", distinct=True)
        )

    def add_rating(self):
        return self.annotate(
            rating=Avg("modules__lessons__review_lesson__rating", distinct=True)
        )

    def add_technologies(self):
        return self.annotate(
            technologies_names=ArrayAgg(
                "modules__lessons__technologies__name", distinct=True
            )
        )

    def add_lecturers(self):
        return self.annotate(
            lecturers_ids=ArrayAgg(
                "modules__lessons__teaching_lesson__lecturer__id", distinct=True
            )
        )

    def add_progress(self, user):
        if not user.is_authenticated:
            return self.annotate(progress=Value(None, output_field=FloatField()))

        profile = Profile.objects.get(user=user)
        if not profile.user_type[0] == "S":
            return self.annotate(progress=Value(None, output_field=FloatField()))

        student_lessons = Reservation.objects.filter(
            student__profile__user=user,
            lesson__in=OuterRef("modules__lessons__id"),
            schedule__end_time__lte=make_aware(datetime.now()),
        ).values("lesson")

        return self.annotate(
            progress=Cast(Count(student_lessons, distinct=True), FloatField())
            / Cast(Count("modules__lessons__id", distinct=True), FloatField())
        )


class CourseManager(Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def add_price(self):
        return self.get_queryset().add_price()

    def add_duration(self):
        return self.get_queryset().add_duration()

    def add_lessons(self):
        return self.get_queryset().add_lessons()

    def add_students_count(self):
        return self.get_queryset().add_students_count()

    def add_rating_count(self):
        return self.get_queryset().add_rating_count()

    def add_rating(self):
        return self.get_queryset().add_rating()

    def add_technologies(self):
        return self.get_queryset().add_technologies()

    def add_lecturers(self):
        return self.get_queryset().add_lecturers()

    def add_progress(self, user):
        return self.get_queryset().add_progress(user=user)


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
    modules = ManyToManyField(Module, related_name="course_modules")

    objects = CourseManager()

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
