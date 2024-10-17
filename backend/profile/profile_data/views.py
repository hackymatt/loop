from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsLecturer
from profile.profile_data.serializers import LecturerProfileDataSerializer
from profile.models import Profile, LecturerProfile


class ProfileDataViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = LecturerProfile.objects.all()
    serializer_class = LecturerProfileDataSerializer
    permission_classes = [IsAuthenticated, IsLecturer]

    def list(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = LecturerProfileDataSerializer(
            LecturerProfile.objects.get(profile=profile), context={"request": request}
        )

        return Response(serializer.data)

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return LecturerProfile.objects.get(profile=profile)
