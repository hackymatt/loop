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
