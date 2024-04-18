from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsStudent
from profile.earnings.serializers import (
    LecturerEarningSerializer,
    EarningByLecturerSerializer,
    AdminEarningLecturerSerializer,
)
from reservation.models import Reservation
from profile.models import Profile
from schedule.models import Schedule
from purchase.models import Purchase
from lesson.models import Lesson
from finance.models import Finance, FinanceHistory
from django.db.models.functions.datetime import ExtractMonth, ExtractYear
from django.db.models import (
    OuterRef,
    Subquery,
    Sum,
    Value,
    F,
    Case,
    When,
    Exists,
    FloatField,
    Func,
    DateTimeField,
)
from django.db.models.functions import Cast
from django.db.models.lookups import GreaterThan
from datetime import datetime, timedelta
from pytz import utc


class EarningViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Schedule.objects.filter(lesson__isnull=False).all()
    serializer_class = LecturerEarningSerializer
    permission_classes = [IsAuthenticated, ~IsStudent]

    def is_total_earnings(self):
        query_params = self.request.query_params
        total = query_params.get("total", True)
        return bool(total)

    def get_serializer_class(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile.user_type[0] == "A":
            if self.is_total_earnings():
                return AdminEarningLecturerSerializer
            return EarningByLecturerSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)

        if profile.user_type[0] == "W":
            queryset = self.queryset.filter(lecturer=profile)
            total_earnings = True
        else:
            queryset = self.queryset
            total_earnings = self.is_total_earnings()

        purchases = (
            Reservation.objects.filter(schedule=OuterRef(OuterRef("pk")))
            .values("purchase")
            .distinct()
        )

        price = (
            Purchase.objects.filter(id__in=Subquery(purchases))
            .annotate(dummy_group_by=Value(1))
            .values("dummy_group_by")
            .order_by("dummy_group_by")
            .annotate(total_price=Sum("price"))
            .values("total_price")
        )

        hours = Lesson.objects.filter(pk=OuterRef("lesson")).values("duration")

        history_rate = FinanceHistory.objects.filter(
            lecturer=OuterRef("lecturer"), created_at__gte=OuterRef("end_time")
        ).order_by("created_at")
        current_rate = Finance.objects.filter(lecturer=OuterRef("lecturer"))

        history_commission = FinanceHistory.objects.filter(
            lecturer=OuterRef("lecturer"), created_at__gte=OuterRef("end_time")
        ).order_by("-created_at")
        current_commission = Finance.objects.filter(lecturer=OuterRef("lecturer"))

        queryset = (
            queryset.annotate(
                month=ExtractMonth("end_time"), year=ExtractYear("end_time")
            )
            .annotate(
                billing_date=Value(
                    datetime.now().replace(
                        day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=utc
                    )
                    - timedelta(days=1)
                )
            )
            .annotate(
                earning_date=Func(
                    F("end_time"),
                    Value("yyyy-MM-01T00:00:00Z"),
                    function="to_char",
                    output_field=DateTimeField(),
                )
            )
            .annotate(
                actual=GreaterThan(
                    F("billing_date"), Cast(F("earning_date"), DateTimeField())
                )
            )
            .annotate(hours=Cast(Subquery(hours), FloatField()) / 60)
            .annotate(price=Subquery(price))
            .annotate(
                rate=Case(
                    When(
                        Exists(history_rate),
                        then=Subquery(history_rate[:1].values("rate")),
                    ),
                    default=Subquery(current_rate.values("rate")),
                )
            )
            .annotate(
                commission=Case(
                    When(
                        Exists(history_commission),
                        then=Subquery(history_commission[:1].values("commission")),
                    ),
                    default=Subquery(current_commission.values("commission")),
                )
            )
            .annotate(
                total_cost=Cast(F("hours") * F("rate"), FloatField())
                + Cast(F("price") * F("commission") / 100, FloatField())
            )
            .annotate(total_profit=F("price"))
        )

        if not total_earnings:
            queryset = queryset.values("actual", "month", "year", "lecturer")
        else:
            queryset = queryset.values("actual", "month", "year")

        queryset = queryset.annotate(cost=Sum("total_cost")).annotate(
            profit=Sum("total_profit")
        )

        if not total_earnings:
            queryset = queryset.values(
                "month", "year", "cost", "profit", "actual", "lecturer"
            )
        else:
            queryset = queryset.values("month", "year", "cost", "profit", "actual")

        return queryset.order_by("-year", "-month")
