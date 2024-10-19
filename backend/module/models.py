from core.base_model import BaseModel
from django.db.models import (
    CharField,
    ManyToManyField,
    Index,
    QuerySet,
    Manager,
    Count,
    Sum,
    Value,
    FloatField,
    OuterRef,
    DecimalField,
    F,
    Subquery,
)
from lesson.models import Lesson
from profile.models import Profile
from reservation.models import Reservation
from django.db.models.functions import Cast
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models.functions import Coalesce


class ModuleQuerySet(QuerySet):
    def add_lessons_count(self):
        return self.annotate(lessons_count=Count("lessons"))

    def add_price(self):
        return self.annotate(price=Sum("lessons__price"))

    def add_progress(self, user):
        if not user.is_authenticated:
            return self.annotate(progress=Value(None, output_field=FloatField()))

        profile = Profile.objects.get(user=user)
        if not profile.user_type[0] == "S":
            return self.annotate(progress=Value(None, output_field=FloatField()))

        student_lessons = Reservation.objects.filter(
            student__profile__user=user,
            lesson__in=OuterRef("lessons__id"),
            schedule__end_time__lte=make_aware(datetime.now()),
        ).values("lesson")

        return self.annotate(
            progress=Cast(Count(student_lessons, distinct=True), FloatField())
            / Cast(Count("lessons__id", distinct=True), FloatField())
        )


class ModuleManager(Manager):
    def get_queryset(self):
        return ModuleQuerySet(self.model, using=self._db)

    def add_lessons_count(self):
        return self.get_queryset().add_lessons_count()

    def add_price(self):
        return self.get_queryset().add_price()

    def add_progress(self, user):
        return self.get_queryset().add_progress(user=user)


class Module(BaseModel):
    title = CharField()
    lessons = ManyToManyField(Lesson, related_name="module_lessons")

    objects = ModuleManager()

    class Meta:
        db_table = "module"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]
