from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile.details.serializers import (
    ProfileDetailsSerializer,
)
from profile.models import Profile


class ProfileDetailsViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileDetailsSerializer(profile, context={"request": request})

        return Response(serializer.data)

    def get_object(self):
        user = self.request.user
        return Profile.objects.get(user=user)
