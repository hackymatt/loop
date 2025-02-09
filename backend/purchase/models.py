from core.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    DecimalField,
    UUIDField,
    BigIntegerField,
    IntegerField,
    CharField,
    SET,
    PROTECT,
    Index,
    QuerySet,
    Manager,
    Case,
    When,
    Value,
    F,
    OuterRef,
    Subquery,
    Exists,
)
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce, Now
from lesson.models import Lesson
from profile.models import StudentProfile
from schedule.models import Recording
from review.models import Review
from config_global import DUMMY_STUDENT_EMAIL, CANCELLATION_TIME
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import uuid


def get_dummy_student_profile():
    return StudentProfile.objects.get(profile__user__email=DUMMY_STUDENT_EMAIL)


class Payment(BaseModel):
    STATUS_CHOICES = (
        ("P", "Pending"),
        ("S", "Success"),
        ("F", "Failure"),
    )
    CURRENCY_CHOICES = (
        ("PLN", "PLN"),
        ("EUR", "EUR"),
        ("USD", "USD"),
    )
    session_id = UUIDField(default=uuid.uuid4)
    order_id = BigIntegerField(null=True, default=None)
    amount = IntegerField()
    currency = CharField(max_length=3, choices=CURRENCY_CHOICES, default="PLN")
    status = CharField(choices=STATUS_CHOICES, default="P")

    class Meta:
        db_table = "payment"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "session_id",
                ]
            ),
            Index(
                fields=[
                    "order_id",
                ]
            ),
        ]


class PurchaseQuerySet(QuerySet):
    def add_meeting_url(self):
        return self.annotate(
            meeting_url=Case(
                When(
                    reservation_purchase__schedule__meeting__isnull=True,
                    then=Value(None),
                ),
                default=F("reservation_purchase__schedule__meeting__url"),
                output_field=CharField(),
            )
        )

    def add_lecturer_id(self):
        return self.annotate(
            lecturer_id=Case(
                When(
                    reservation_purchase__schedule__lesson__isnull=True,
                    then=Value(None),
                ),
                default=F("reservation_purchase__schedule__lecturer__id"),
                output_field=IntegerField(),
            )
        )

    def add_recordings_ids(self):
        recordings_subquery = (
            Recording.objects.filter(
                schedule=OuterRef("reservation_purchase__schedule")
            )
            .annotate(ids=ArrayAgg("id"))
            .values("ids")
        )
        return self.annotate(recordings_ids=Coalesce(Subquery(recordings_subquery), []))

    def add_reservation_id(self):
        return self.annotate(
            reservation_id=Case(
                When(reservation_purchase__isnull=True, then=Value(None)),
                default=F("reservation_purchase__id"),
                output_field=IntegerField(),
            )
        )

    def add_review_id(self):
        review_subquery = Review.objects.filter(
            student=OuterRef("student"), lesson=OuterRef("lesson")
        )
        return self.annotate(
            review_id=Case(
                When(~Exists(review_subquery), then=Value(None)),
                default=Subquery(review_subquery.values("id")[:1]),
                output_field=IntegerField(),
            )
        )

    def add_lesson_status(self):
        return self.annotate(
            lesson_status=Case(
                When(
                    reservation_purchase__schedule__end_time__lte=Now(),
                    then=Value("zakończona"),
                ),
                When(
                    reservation_purchase__schedule__start_time__lte=Now()
                    + timedelta(hours=CANCELLATION_TIME),
                    then=Value("potwierdzona"),
                ),
                When(
                    reservation_purchase__schedule__start_time__gt=Now(),
                    then=Value("zaplanowana"),
                ),
                default=Value("nowa"),
                output_field=CharField(),
            )
        )

    def add_review_status(self):
        review_subquery = Review.objects.filter(
            student=OuterRef("student"), lesson=OuterRef("lesson")
        )

        return self.annotate(
            review_status=Case(
                When(
                    lesson_status=Value("zakończona"),
                    then=Case(
                        When(Exists(review_subquery), then=Value("ukończone")),
                        default=Value("oczekujące"),
                        output_field=CharField(),
                    ),
                ),
                default=Value("brak"),
                output_field=CharField(),
            )
        )


class PurchaseManager(Manager):
    def get_queryset(self):
        return PurchaseQuerySet(self.model, using=self._db)


class Purchase(BaseModel):
    lesson = ForeignKey(
        Lesson,
        on_delete=PROTECT,
        related_name="purchase_lesson",
    )
    student = ForeignKey(
        StudentProfile,
        on_delete=SET(get_dummy_student_profile),
        related_name="purchase_student",
    )
    price = DecimalField(max_digits=7, decimal_places=2, null=True)
    payment = ForeignKey(Payment, on_delete=PROTECT, related_name="purchase_payment")

    objects = PurchaseManager()

    class Meta:
        db_table = "purchase"
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
            Index(
                fields=[
                    "student",
                    "lesson",
                ]
            ),
        ]
