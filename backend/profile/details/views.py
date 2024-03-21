from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile.details.serializers import (
    ProfileDetailsSerializer,
    LecturerDetailsSerializer,
)
from profile.models import Profile
from django.contrib.auth.models import User


class ProfileDetailsViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = User.objects.all()
    serializer_class = ProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile.user_type[0] == "S":
            return ProfileDetailsSerializer
        else:
            return LecturerDetailsSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        if profile.user_type[0] == "S":
            serializer = ProfileDetailsSerializer(profile, context={"request": request})
        else:
            serializer = LecturerDetailsSerializer(
                profile, context={"request": request}
            )

        return Response(serializer.data)

    def get_object(self):
        user = self.request.user
        return Profile.objects.get(user=user)
