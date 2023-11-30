from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from utils.permissions.permissions import IsStudent
from teaching.serializers import TeachingSerializer, TeachingGetSerializer
from teaching.models import Teaching
from profile.models import Profile


class TeachingViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Teaching.objects.all()
    serializer_class = TeachingGetSerializer
    permission_classes = [IsAuthenticated & ~IsStudent]

    def get_queryset(self):
        user = self.request.user
        lecturer = Profile.objects.get(user=user)
        return self.queryset.filter(lecturer=lecturer)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        lecturer = Profile.objects.get(user=user)
        data["lecturer"] = lecturer.id
        serializer = TeachingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=TeachingGetSerializer(records, many=True).data,
        )
