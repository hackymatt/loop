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
from profile.models import LecturerProfile
from django.db.models import Count, Prefetch
from django.contrib.auth.models import User
from config_global import DUMMY_STUDENT_EMAIL


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = (
        Review.objects.all()
        .prefetch_related(Prefetch("lecturer", queryset=LecturerProfile.objects.all()))
        .order_by("id")
    )
    filterset_class = ReviewFilter
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ReviewGetSerializer
        return ReviewSerializer

    def get_permissions(self):
        permission_map = {
            "create": [IsAuthenticated],
            "update": [IsAuthenticated, IsUserReview],
            "destroy": [IsAuthenticated, IsUserReview],
        }
        return [
            permission()
            for permission in permission_map.get(self.action, self.permission_classes)
        ]


class ReviewStatsViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Review.objects.all().order_by("id")
    serializer_class = ReviewStatsSerializer
    filterset_class = ReviewFilter
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            self.queryset.values("rating")
            .annotate(count=Count("rating"))
            .order_by("rating")
        )


class BestReviewViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        Review.objects.filter(rating=5, review__isnull=False).all().order_by("id")
    )
    serializer_class = BestReviewSerializer

    def get_queryset(self):
        dummy_user = User.objects.get(email=DUMMY_STUDENT_EMAIL)
        queryset = self.queryset.exclude(student__profile__user=dummy_user)
        random_ids = queryset.order_by("?").values_list("id", flat=True)[:10]
        return queryset.filter(id__in=random_ids)
