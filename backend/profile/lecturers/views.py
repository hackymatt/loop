from rest_framework.viewsets import ModelViewSet
from profile.lecturers.serializers import (
    LecturerSerializer,
    LecturerGetSerializer,
    BestLecturerSerializer,
)
from profile.lecturers.filters import LecturerFilter
from profile.models import LecturerProfile
from review.models import Review
from django.db.models import OuterRef, Subquery, Value, Avg
from django.contrib.auth.models import User
from django.conf import settings
from random import sample


class LecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LecturerProfile.objects.all()
    serializer_class = LecturerSerializer
    filterset_class = LecturerFilter
    search_fields = [
        "profile__user__first_name",
        "profile__user__last_name",
        "profile__user__email",
        "title",
    ]

    def get_queryset(self):
        dummy_user = User.objects.get(email=settings.DUMMY_LECTURER_EMAIL)
        return self.queryset.exclude(profile__user=dummy_user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LecturerGetSerializer
        else:
            return self.serializer_class


class BestLecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LecturerProfile.objects.all()
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
        dummy_user = User.objects.get(email=settings.DUMMY_LECTURER_EMAIL)
        queryset = self.queryset.exclude(profile__user=dummy_user)

        queryset = self.get_rating(queryset=queryset).filter(rating__gte=4)

        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 4))
        return queryset.filter(id__in=random_ids)
