from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from review.permissions import IsUserReview
from review.serializers import (
    ReviewSerializer,
    ReviewGetSerializer,
    ReviewStatsSerializer,
    BestReviewSerializer,
)
from review.filters import ReviewFilter
from review.models import Review
from random import sample
from django.db.models import Count, Prefetch
from django.contrib.auth.models import User
from config_global import DUMMY_STUDENT_EMAIL
from profile.models import LecturerProfile


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = (
        Review.objects.prefetch_related("student")
        .prefetch_related(
            Prefetch("lecturer", queryset=LecturerProfile.objects.add_full_name())
        )
        .prefetch_related("lesson")
        .all()
        .order_by("rating")
    )
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ReviewGetSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "destroy"]:
            permission_classes = [IsAuthenticated, IsUserReview]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class ReviewStatsViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        Review.objects.values("rating")
        .annotate(count=Count("rating"))
        .order_by("rating")
    )
    serializer_class = ReviewStatsSerializer
    filterset_class = ReviewFilter
    permission_classes = [AllowAny]


class BestReviewViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        Review.objects.filter(rating=5, review__isnull=False).all().order_by("rating")
    )
    serializer_class = BestReviewSerializer

    def get_queryset(self):
        dummy_user = User.objects.get(email=DUMMY_STUDENT_EMAIL)

        queryset = self.queryset.exclude(student__profile__user=dummy_user)
        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return self.queryset.filter(id__in=random_ids)
