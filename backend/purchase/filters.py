from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    UUIDFilter,
    DateFilter,
)
from review.models import Review
from purchase.models import LessonPurchase
from profile.models import Profile
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


def get_lesson_lecturer(queryset):
    lecturer = Profile.objects.filter(pk=OuterRef("lecturer")).values("uuid")

    schedule = (
        Schedule.objects.filter(pk=OuterRef("schedule"))
        .annotate(lecturer_uuid=Subquery(lecturer))
        .values("lecturer_uuid")
    )

    reservation = Reservation.objects.filter(
        student=OuterRef("student"), lesson=OuterRef("lesson")
    ).annotate(lecturer_uuid=Subquery(schedule))

    purchase = queryset.annotate(
        lecturer_exists=Subquery(Exists(reservation))
    ).annotate(
        lecturer_uuid=Case(
            When(
                lecturer_exists=1,
                then=Cast(Subquery(reservation.values("lecturer_uuid")), CharField()),
            ),
            When(lecturer_exists=None, then=Value("")),
        )
    )

    return purchase


def get_lesson_status(queryset):
    schedule = (
        Schedule.objects.filter(pk=OuterRef("schedule"))
        .annotate(diff=datetime.now().date() - F("time"))
        .values("diff")
    )

    reservation = Reservation.objects.filter(
        student=OuterRef("student"), lesson=OuterRef("lesson")
    ).annotate(diff=Extract(Subquery(schedule), "epoch"))

    purchase = (
        queryset.annotate(reservation_exists=Subquery(Exists(reservation)))
        .annotate(diff=Subquery(reservation.values("diff")))
        .annotate(
            lesson_status=Case(
                When(diff__gte=0, then=Value(LessonStatus.COMPLETED)),
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
            elif value in ["lecturer_uuid", "-lecturer_uuid"]:
                queryset = get_lesson_lecturer(queryset).order_by(value)
            elif value in ["course_title", "-course_title"]:
                value_modified = value.replace("course_", "course_purchase__course__")
                queryset = queryset.order_by(value_modified)
            elif value in ["lesson_title", "-lesson_title"]:
                value_modified = value.replace("lesson_", "lesson__")
                queryset = queryset.order_by(value_modified)
            else:
                queryset = queryset.order_by(value)

        return queryset


class PurchaseFilter(FilterSet):
    course_title = CharFilter(
        field_name="course_purchase__course__title", lookup_expr="icontains"
    )
    lesson_title = CharFilter(field_name="lesson__title", lookup_expr="icontains")
    lesson_status = CharFilter(
        label="Lesson status",
        field_name="lesson_status",
        method="filter_lesson_status",
    )
    lecturer_id = UUIDFilter(
        label="Lecturer Id",
        field_name="lecturer_uuid",
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
            ("course_title", "Course Title ASC"),
            ("-course_title", "Course Title DESC"),
            ("lesson_title", "Lesson Title ASC"),
            ("-lesson_title", "Lesson Title DESC"),
            ("lesson_status", "Lesson Status ASC"),
            ("-lesson_status", "Lesson Status DESC"),
            ("review_status", "Review Status ASC"),
            ("-review_status", "Review Status DESC"),
            ("lecturer_uuid", "Lecturer Id ASC"),
            ("-lecturer_uuid", "Lecturer Id DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "course_title": "course_title",
            "-course_title": "-course_title",
            "lesson_title": "lesson_title",
            "lesson_title": "-lesson_title",
            "lesson_status": "lesson_status",
            "lesson_status": "-lesson_status",
            "review_status": "review_status",
            "review_status": "-review_status",
            "lecturer_uuid": "lecturer_uuid",
            "lecturer_uuid": "-lecturer_uuid",
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = LessonPurchase
        fields = (
            "course_title",
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
