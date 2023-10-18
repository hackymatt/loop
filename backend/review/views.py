from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from review.serializers import ReviewSerializer, BestReviewSerializer
from review.models import Review
from course.models import Lesson
from profile.models import Profile


class ReviewViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if self.action == "list":
            course_id = self.request.query_params.get("course_id", None)
            if course_id:
                lessons = Lesson.objects.filter(course_id=course_id).all()
                return self.queryset.filter(lesson__in=lessons).all()
            else:
                return self.queryset

        return self.queryset

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

        # TODO: check if user bought the lesson

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
