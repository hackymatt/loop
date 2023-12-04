from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from review.permissions import IsUserReview
from review.serializers import (
    ReviewSerializer,
    ReviewGetSerializer,
    BestReviewSerializer,
)
from review.filters import ReviewFilter
from review.models import Review
from random import sample


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


class BestReviewViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Review.objects.filter(rating=5, review__isnull=False).all()
    serializer_class = BestReviewSerializer

    def get_queryset(self):
        ids = self.queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return self.queryset.filter(id__in=random_ids)
