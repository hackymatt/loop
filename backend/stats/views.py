from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.models import Profile
from course.models import Course
from lesson.models import Lesson, Technology
from review.models import Review
from purchase.models import Purchase
from django.db.models import Sum, Avg


class StatsViewSet(ViewSet):
    http_method_names = ["get"]

    def get_stats(self, request):
        students_count = Profile.objects.filter(user_type__startswith="S").count()
        course_count = Course.objects.count()
        lessons_count = Lesson.objects.count()
        technology_count = Technology.objects.count()
        lecturers_count = Profile.objects.filter(user_type__startswith="W").count()
        purchase_count = Purchase.objects.count()
        hours_sum = Lesson.objects.aggregate(Sum("duration"))["duration__sum"]
        rating = Review.objects.aggregate(Avg("rating"))["rating__avg"]
        rating_count = Review.objects.count()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "students_count": students_count,
                "course_count": course_count,
                "lessons_count": lessons_count,
                "technology_count": technology_count,
                "lecturers_count": lecturers_count,
                "purchase_count": purchase_count,
                "hours_sum": hours_sum if hours_sum else 0,
                "rating": rating if rating else 0,
                "rating_count": rating_count,
            },
        )
