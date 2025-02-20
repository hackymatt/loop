from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profile.personal_data.serializers import (
    ProfileDetailsSerializer,
)
from profile.models import Profile
from const import UserType


class PersonalDataViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Profile.objects.all().order_by("id")
    serializer_class = ProfileDetailsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileDetailsSerializer(profile, context={"request": request})
        data = serializer.data

        if profile.user_type == UserType.STUDENT:
            del data["user_type"]

        return Response(data)

    def get_object(self):
        user = self.request.user
        return Profile.objects.get(user=user)
