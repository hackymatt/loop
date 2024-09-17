from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    NumberFilter,
    DateFilter,
)
from review.models import Review
from purchase.models import Purchase
from profile.models import LecturerProfile
from django.db.models import (
    OuterRef,
    Subquery,
    Value,
    Exists,
    Case,
    When,
    F,
    CharField,
    Q,
)
from django.db.models.functions import Cast, Extract
from reservation.models import Reservation
from purchase.serializers import LessonStatus, ReviewStatus
from datetime import datetime
from schedule.models import Schedule
from const import CANCELLATION_TIME


def get_lesson_lecturer(queryset):
    lecturer = (
        LecturerProfile.objects.exclude(
            Q(title__isnull=True) | Q(description__isnull=True)
        )
        .filter(pk=OuterRef("lecturer"))
        .values("id")
    )

    schedule = (
        Schedule.objects.filter(pk=OuterRef("schedule"))
        .annotate(teacher_id=Subquery(lecturer))
        .values("teacher_id")
    )

    reservation = Reservation.objects.filter(purchase__pk=OuterRef("pk")).annotate(
        teacher_id=Subquery(schedule)
    )

    purchase = queryset.annotate(
        lecturer_exists=Subquery(Exists(reservation))
    ).annotate(
        teacher_id=Case(
            When(
                lecturer_exists=1,
                then=Cast(Subquery(reservation.values("teacher_id")), CharField()),
            ),
            When(lecturer_exists=None, then=Value("")),
        )
    )

    return purchase


def get_lesson_status(queryset):
    start_schedule = (
        Schedule.objects.filter(pk=OuterRef("schedule"))
        .annotate(diff=datetime.now() - F("start_time"))
        .values("diff")
    )
    end_schedule = (
        Schedule.objects.filter(pk=OuterRef("schedule"))
        .annotate(diff=datetime.now() - F("end_time"))
        .values("diff")
    )

    reservation = (
        Reservation.objects.filter(purchase__pk=OuterRef("pk"))
        .annotate(start_diff=Extract(Subquery(start_schedule), "epoch"))
        .annotate(end_diff=Extract(Subquery(end_schedule), "epoch"))
    )

    purchase = (
        queryset.annotate(reservation_exists=Subquery(Exists(reservation)))
        .annotate(start_diff=Subquery(reservation.values("start_diff")))
        .annotate(end_diff=Subquery(reservation.values("end_diff")))
        .annotate(
            lesson_status=Case(
                When(end_diff__gte=0, then=Value(LessonStatus.COMPLETED)),
                When(
                    start_diff__gte=-CANCELLATION_TIME * 60 * 60,
                    then=Value(LessonStatus.CONFIRMED),
                ),
                When(reservation_exists=1, then=Value(LessonStatus.PLANNED)),
                default=Value(LessonStatus.NEW),
            )
        )
    )

    return purchase


def get_review_status(queryset):
    found = Exists(
        Review.objects.filter(student=OuterRef("student"), lesson=OuterRef("lesson"))
    )
    purchase = queryset.annotate(review_exists=Subquery(found)).annotate(
        review_status=Case(
            When(
                ~Q(lesson_status=LessonStatus.COMPLETED),
                then=Value(ReviewStatus.NONE),
            ),
            When(review_exists=1, then=Value(ReviewStatus.COMPLETED)),
            When(review_exists=None, then=Value(ReviewStatus.NOT_COMPLETED)),
        )
    )

    return purchase


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["review_status", "-review_status"]:
                queryset = get_review_status(get_lesson_status(queryset)).order_by(
                    value
                )
            elif value in ["lesson_status", "-lesson_status"]:
                queryset = get_lesson_status(queryset).order_by(value)
            elif value in ["lecturer_id", "-lecturer_id"]:
                value_modified = value.replace("lecturer", "teacher")
                queryset = get_lesson_lecturer(queryset).order_by(value_modified)
            elif value in ["lesson_title", "-lesson_title"]:
                value_modified = value.replace("lesson_", "lesson__")
                queryset = queryset.order_by(value_modified)
            else:
                queryset = queryset.order_by(value)

        return queryset


class PurchaseFilter(FilterSet):
    lesson_title = CharFilter(field_name="lesson__title", lookup_expr="icontains")
    lesson_status = CharFilter(
        label="Lesson status",
        field_name="lesson_status",
        method="filter_lesson_status",
    )
    lecturer_id = NumberFilter(
        label="Lecturer Id",
        field_name="teacher_id",
        method="filter_lecturer_id",
    )
    review_status = CharFilter(
        label="Review status",
        field_name="review_status",
        method="filter_review_status",
    )
    review_status_exclude = CharFilter(
        label="Review status exclude",
        field_name="review_status",
        method="filter_review_status_exclude",
    )
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")

    sort_by = OrderFilter(
        choices=(
            ("lesson_title", "Lesson Title ASC"),
            ("-lesson_title", "Lesson Title DESC"),
            ("lesson_status", "Lesson Status ASC"),
            ("-lesson_status", "Lesson Status DESC"),
            ("review_status", "Review Status ASC"),
            ("-review_status", "Review Status DESC"),
            ("lecturer_id", "Lecturer Id ASC"),
            ("-lecturer_id", "Lecturer Id DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "lesson_title": "lesson_title",
            "lesson_title": "-lesson_title",
            "lesson_status": "lesson_status",
            "lesson_status": "-lesson_status",
            "review_status": "review_status",
            "review_status": "-review_status",
            "lecturer_id": "lecturer_id",
            "lecturer_id": "-lecturer_id",
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = Purchase
        fields = (
            "lesson_title",
            "lesson_status",
            "lecturer_id",
            "review_status",
            "review_status_exclude",
            "created_at",
            "sort_by",
        )

    def filter_review_status(self, queryset, field_name, value):
        lookup_field_name = field_name
        return get_review_status(get_lesson_status(queryset)).filter(
            **{lookup_field_name: value}
        )

    def filter_review_status_exclude(self, queryset, field_name, value):
        lookup_field_name = field_name
        return get_review_status(get_lesson_status(queryset)).exclude(
            **{lookup_field_name: value}
        )

    def filter_lesson_status(self, queryset, field_name, value):
        lookup_field_name = field_name
        return get_lesson_status(queryset).filter(**{lookup_field_name: value})

    def filter_lecturer_id(self, queryset, field_name, value):
        lookup_field_name = field_name
        return get_lesson_lecturer(queryset).filter(**{lookup_field_name: value})
