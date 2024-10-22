from rest_framework.viewsets import ModelViewSet
from profile.lecturers.serializers import (
    LecturerSerializer,
    LecturerGetSerializer,
    BestLecturerSerializer,
)
from profile.lecturers.filters import LecturerFilter
from profile.models import LecturerProfile
from random import sample
from config_global import DUMMY_LECTURER_EMAIL


class LecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        LecturerProfile.objects.add_profile_ready()
        .add_lessons_count()
        .filter(lessons_count__gt=0, profile_ready=True)
        .exclude(profile__user__email=DUMMY_LECTURER_EMAIL)
        .add_full_name()
        .add_rating()
        .add_rating_count()
        .add_lessons_duration()
        .add_students_count()
        .order_by("id")
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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LecturerGetSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.add_lessons().add_lessons_price()
        return self.queryset


class BestLecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        LecturerProfile.objects.add_profile_ready()
        .add_full_name()
        .add_rating()
        .filter(rating__gte=4)
        .exclude(profile_ready=False, profile__user__email=DUMMY_LECTURER_EMAIL)
        .all()
        .order_by("id")
    )
    serializer_class = BestLecturerSerializer

    def get_queryset(self):
        ids = self.queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 4))
        return self.queryset.filter(id__in=random_ids)
