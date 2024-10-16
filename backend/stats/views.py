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
        students_count = max(StudentProfile.objects.count() - 1, 0)
        lecturers_count = max(LecturerProfile.objects.count() - 1, 0)

        course_count = Course.objects.count()
        lessons_count = Lesson.objects.count()
        technology_count = Technology.objects.count()
        purchase_count = Purchase.objects.filter(payment__status="S").count()

        duration = Lesson.objects.aggregate(
            total_duration=Sum("duration"),
        )
        rating = Lesson.objects.aggregate(average_rating=Avg("review__rating"))

        # Calculate hours and set defaults if no lessons or ratings exist
        hours_sum = (
            (duration["total_duration"] / 60) if duration["total_duration"] else 0
        )
        rating = rating["average_rating"] or 0
        rating_count = Review.objects.count()

        # Build response data
        response_data = {
            "students_count": students_count,
            "course_count": course_count,
            "lessons_count": lessons_count,
            "technology_count": technology_count,
            "lecturers_count": lecturers_count,
            "purchase_count": purchase_count,
            "hours_sum": hours_sum,
            "rating": rating,
            "rating_count": rating_count,
        }

        return Response(status=status.HTTP_200_OK, data=response_data)
