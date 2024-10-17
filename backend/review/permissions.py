from rest_framework.permissions import BasePermission
from profile.models import Profile, StudentProfile


class IsUserReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        profile = Profile.objects.get(user=user)

        return obj.student == StudentProfile.objects.get(profile=profile)
