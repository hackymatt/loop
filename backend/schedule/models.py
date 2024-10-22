from core.base_model import BaseModel
from django.db.models import (
    UniqueConstraint,
    OneToOneField,
    ForeignKey,
    DateTimeField,
    CharField,
    URLField,
    CASCADE,
    PROTECT,
    Index,
    QuerySet,
    Manager,
    F,
    Value,
    Case,
    When,
    Count,
)
from django.db.models.functions import ExtractYear, ExtractMonth, Concat, Right
from django.contrib.postgres.aggregates import ArrayAgg
from profile.models import LecturerProfile
from lesson.models import Lesson
from datetime import datetime
from django.utils.timezone import make_aware


class Meeting(BaseModel):
    event_id = CharField(unique=True)
    url = URLField()

    class Meta:
        db_table = "meeting"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "event_id",
                ]
            ),
            Index(
                fields=[
                    "url",
                ]
            ),
        ]


class ScheduleQuerySet(QuerySet):
    def add_diff(self):
        return self.annotate(diff=make_aware(datetime.now()) - F("start_time"))

    def add_year_month(self):
        return self.annotate(
            year_month=Concat(
                ExtractYear(F("start_time")),
                Value("-"),
                Right(Concat(Value("0"), ExtractMonth(F("start_time"))), 2),
                output_field=CharField(),
            )
        )

    def add_meeting_url(self):
        return self.annotate(
            meeting_url=Case(
                When(meeting__isnull=False, then=F("meeting__url")),
                default=Value(None),
                output_field=CharField(),
            )
        )

    def add_reservations_count(self):
        return self.annotate(
            reservations_count=Count("reservation_schedule", distinct=True)
        )

    def add_students_ids(self):
        return self.annotate(
            students_ids=ArrayAgg("reservation_schedule__student", distinct=True)
        )


class ScheduleManager(Manager):
    def get_queryset(self):
        return ScheduleQuerySet(self.model, using=self._db)

    def add_diff(self):
        return self.get_queryset().add_diff()


class Schedule(BaseModel):
    lecturer = ForeignKey(
        LecturerProfile, on_delete=CASCADE, related_name="schedule_lecturer"
    )
    start_time = DateTimeField()
    end_time = DateTimeField()
    lesson = ForeignKey(
        Lesson, on_delete=PROTECT, related_name="schedule_lesson", null=True, blank=True
    )
    meeting = OneToOneField(Meeting, on_delete=CASCADE, null=True, blank=True)

    objects = ScheduleManager()

    class Meta:
        db_table = "schedule"
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["lecturer", "start_time", "end_time"],
                name="schedule_lecturer_time_unique_together",
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
                    "lecturer",
                ]
            ),
            Index(
                fields=[
                    "lesson",
                ]
            ),
            Index(
                fields=[
                    "lesson",
                    "lecturer",
                ]
            ),
        ]


class Recording(BaseModel):
    schedule = ForeignKey(
        Schedule, on_delete=CASCADE, related_name="recording_schedule"
    )
    file_id = CharField()
    file_name = CharField()
    file_url = URLField()

    class Meta:
        db_table = "recording"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "file_id",
                ]
            ),
            Index(
                fields=[
                    "file_name",
                ]
            ),
        ]
