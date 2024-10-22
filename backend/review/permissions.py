from rest_framework.permissions import BasePermission


class IsUserReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.student.profile.user == user
