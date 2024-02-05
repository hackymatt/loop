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
from profile.models import Profile
from random import sample
from django.db.models import Count


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Review.objects.all()
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
        elif self.action == "update" or self.action == "destroy":
            permission_classes = [IsAuthenticated & IsUserReview]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == "list":
            course_id = self.request.query_params.get("course_id", None)
            if not course_id:
                user = self.request.user
                if user.is_authenticated:
                    student = Profile.objects.get(user=user)
                    return self.queryset.filter(student=student)
                else:
                    return self.queryset
            else:
                return self.queryset
        else:
            return self.queryset


class ReviewStatsViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Review.objects.all()
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
    queryset = Review.objects.filter(rating=5, review__isnull=False).all()
    serializer_class = BestReviewSerializer

    def get_queryset(self):
        ids = self.queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return self.queryset.filter(id__in=random_ids)
