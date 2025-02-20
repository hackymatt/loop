from rest_framework.permissions import BasePermission
from profile.models import Profile
from const import UserType


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = Profile.objects.get(user=user)

        return profile.user_type == UserType.STUDENT


class IsLecturer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = Profile.objects.get(user=user)

        return profile.user_type == UserType.INSTRUCTOR
