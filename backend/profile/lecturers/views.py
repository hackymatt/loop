from rest_framework.viewsets import ModelViewSet
from profile.lecturers.serializers import (
    LecturerSerializer,
    LecturerGetSerializer,
    BestLecturerSerializer,
)
from profile.lecturers.filters import LecturerFilter
from profile.models import LecturerProfile
from review.models import Review
from teaching.models import Teaching
from django.db.models import OuterRef, Subquery, Value, Avg, Count, Q
from django.contrib.auth.models import User
from random import sample
from config_global import DUMMY_LECTURER_EMAIL


class LecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LecturerProfile.objects.all().exclude(
        Q(title__isnull=True) | Q(description__isnull=True)
    )
    serializer_class = LecturerSerializer
    filterset_class = LecturerFilter
    search_fields = [
        "profile__user__first_name",
        "profile__user__last_name",
        "profile__user__email",
        "title",
        "description",
    ]

    def get_queryset(self):
        total_lessons_count = (
            Teaching.objects.filter(lecturer=OuterRef("pk"))
            .annotate(dummy_group_by=Value(1))
            .values("dummy_group_by")
            .order_by("dummy_group_by")
            .annotate(total_lessons_count=Count("pk"))
            .values("total_lessons_count")
        )

        dummy_user = User.objects.get(email=DUMMY_LECTURER_EMAIL)
        queryset = self.queryset.exclude(profile__user=dummy_user)
        return (
            queryset.annotate(lessons_count=Subquery(total_lessons_count))
            .filter(lessons_count__gt=0)
            .order_by("id")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LecturerGetSerializer
        return self.serializer_class


class BestLecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LecturerProfile.objects.exclude(
        Q(title__isnull=True) | Q(description__isnull=True)
    ).all()
    serializer_class = BestLecturerSerializer

    def get_rating(self, queryset):
        avg_rating = (
            Review.objects.filter(lecturer=OuterRef("pk"))
            .annotate(dummy_group_by=Value(1))
            .values("dummy_group_by")
            .order_by("dummy_group_by")
            .annotate(avg_rating=Avg("rating"))
            .values("avg_rating")
        )
        lecturers = queryset.annotate(rating=Subquery(avg_rating))

        return lecturers

    def get_queryset(self):
        dummy_user = User.objects.get(email=DUMMY_LECTURER_EMAIL)
        queryset = self.queryset.exclude(profile__user=dummy_user)

        queryset = self.get_rating(queryset=queryset).filter(rating__gte=4)

        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 4))
        return queryset.filter(id__in=random_ids)
