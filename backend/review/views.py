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
from django.contrib.auth.models import User
from django.conf import settings


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

    def set_lecturer(self, request):
        data = request.data
        lecturer_uuid = data["lecturer"]
        lecturer = Profile.objects.get(uuid=lecturer_uuid)
        data["lecturer"] = lecturer.id

        return request

    def create(self, request, *args, **kwargs):
        request = self.set_lecturer(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request = self.set_lecturer(request)
        return super().update(request, *args, **kwargs)


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
        dummy_user = User.objects.get(email=settings.DUMMY_STUDENT_EMAIL)

        queryset = self.queryset.exclude(student__user=dummy_user)
        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return self.queryset.filter(id__in=random_ids)
