from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from utils.filtering.backends import ComplexFilterBackend
from review.serializers import ReviewSerializer, BestReviewSerializer
from review.filters import ReviewFilter
from review.models import Review
from purchase.models import Purchase
from course.models import Lesson
from profile.models import Profile


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (
        ComplexFilterBackend,
        SearchFilter,
    )
    filterset_class = ReviewFilter

    @staticmethod
    def is_lesson_purchased(user, lesson_id):
        profile = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=lesson_id)

        return Purchase.objects.filter(profile=profile, lesson=lesson).exists()

    @staticmethod
    def is_review_created(user, lesson_id):
        profile = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=lesson_id)

        return Review.objects.filter(profile=profile, lesson=lesson).exists()

    @staticmethod
    def is_user_review(user, review):
        profile = Profile.objects.get(user=user)

        return review.profile == profile

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"review": "Użytkownik niezalogowany."},
            )

        if self.is_review_created(user=user, lesson_id=data["lesson"]):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Recenzja już istnieje."},
            )

        if not self.is_lesson_purchased(user=user, lesson_id=data["lesson"]):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Użytkownik nie kupił kursu."},
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"review": "Użytkownik niezalogowany."},
            )

        if not self.is_user_review(user=user, review=self.get_object()):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Brak recenzji."},
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"review": "Użytkownik niezalogowany."},
            )

        if not self.is_user_review(user=user, review=self.get_object()):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Brak recenzji."},
            )

        return super().destroy(request, *args, **kwargs)


class BestReviewViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Review.objects.filter(rating=5, review__isnull=False).all()
    serializer_class = BestReviewSerializer
