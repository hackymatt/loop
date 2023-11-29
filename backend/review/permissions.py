from rest_framework.permissions import BasePermission
from profile.models import Profile
from course.models import Lesson
from purchase.models import LessonPurchase
from review.models import Review


class IsUserReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        profile = Profile.objects.get(user=user)

        return obj.student == profile


class IsLessonPurchased(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        data = request.data
        profile = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=data["lesson"])

        return LessonPurchase.objects.filter(student=profile, lesson=lesson).exists()


class IsReviewExist(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        data = request.data
        student = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=data["lesson"])
        lecturer = Profile.objects.get(pk=data["lecturer"])

        return Review.objects.filter(
            student=student, lesson=lesson, lecturer=lecturer
        ).exists()
