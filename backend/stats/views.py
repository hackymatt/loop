from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profile.models import StudentProfile, LecturerProfile
from course.models import Course
from lesson.models import Lesson, Technology
from review.models import Review
from purchase.models import Purchase
from django.db.models import Sum, Avg


class StatsAPIView(APIView):
    http_method_names = ["get"]

    def get(self, request):
        students_count = StudentProfile.objects.count() - 1
        course_count = Course.objects.count()
        technology_count = Technology.objects.count()
        lecturers_count = LecturerProfile.objects.count() - 1
        purchase_count = Purchase.objects.filter(payment__status="S").count()

        lessons = Lesson.objects.all()
        lessons_count = lessons.count()
        hours_sum = (
            lessons.aggregate(Sum("duration"))["duration__sum"] / 60
            if lessons_count > 0
            else 0
        )
        reviews = Review.objects.all()
        rating = reviews.aggregate(Avg("rating"))["rating__avg"]
        rating_count = reviews.count()

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
