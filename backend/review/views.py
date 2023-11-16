from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from review.serializers import (
    ReviewSerializer,
    ReviewGetSerializer,
    BestReviewSerializer,
)
from review.filters import ReviewFilter
from review.models import Review
from purchase.models import Purchase
from course.models import Lesson
from profile.models import Profile
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from random import sample


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ReviewGetSerializer
        return self.serializer_class

    @staticmethod
    def is_lesson_purchased(user, lesson_id, lecturer_id):
        profile = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=lesson_id)
        lecturer = Profile.objects.get(pk=lecturer_id)

        return Purchase.objects.filter(
            student=profile, lesson=lesson, lecturer=lecturer
        ).exists()

    @staticmethod
    def is_lesson_finished(user, lesson_id, lecturer_id):
        profile = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=lesson_id)
        lecturer = Profile.objects.get(pk=lecturer_id)
        start_time = (
            Purchase.objects.filter(student=profile, lesson=lesson, lecturer=lecturer)
            .first()
            .time.time
        )
        end_time = start_time + timedelta(minutes=lesson.duration)

        return make_aware(datetime.now()) >= end_time

    @staticmethod
    def is_review_created(user, lesson_id, lecturer_id):
        student = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=lesson_id)
        lecturer = Profile.objects.get(pk=lecturer_id)

        return Review.objects.filter(
            student=student, lesson=lesson, lecturer=lecturer
        ).exists()

    @staticmethod
    def is_user_review(user, review):
        profile = Profile.objects.get(user=user)

        return review.student == profile

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"review": "Użytkownik niezalogowany."},
            )

        if self.is_review_created(
            user=user, lesson_id=data["lesson"], lecturer_id=data["lecturer"]
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Recenzja już istnieje."},
            )

        if not self.is_lesson_purchased(
            user=user, lesson_id=data["lesson"], lecturer_id=data["lecturer"]
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Użytkownik nie kupił lekcji."},
            )

        if not self.is_lesson_finished(
            user=user, lesson_id=data["lesson"], lecturer_id=data["lecturer"]
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"review": "Lekcja się nie skończyła."},
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

    def get_queryset(self):
        ids = self.queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return self.queryset.filter(id__in=random_ids)
