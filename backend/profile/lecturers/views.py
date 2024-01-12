from rest_framework.viewsets import ModelViewSet
from profile.lecturers.serializers import (
    LecturerSerializer,
    BestLecturerSerializer,
)
from profile.models import Profile
from review.models import Review
from django.db.models import OuterRef, Subquery, Value, Avg
from random import sample


class LecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Profile.objects.filter(user_type="W").all()
    serializer_class = LecturerSerializer


class BestLecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Profile.objects.filter(user_type="W").all()
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
        queryset = self.queryset
        queryset = self.get_rating(queryset=queryset).filter(rating__gte=4)

        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 4))
        return queryset.filter(id__in=random_ids)
