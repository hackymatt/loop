from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsStudent
from rest_framework import status
from django.http import JsonResponse
from certificate.serializers import CertificateSerializer, CertificateInfoSerializer
from certificate.models import Certificate
from certificate.filters import CertificateFilter
from profile.models import Profile
from django.views.decorators.csrf import csrf_exempt


class CertificateViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Certificate.objects.all().order_by("id")
    serializer_class = CertificateSerializer
    filterset_class = CertificateFilter
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(student__profile__user=user)


class CertificateInfoAPIView(APIView):
    http_method_names = ["get"]

    @csrf_exempt
    def get(self, request, id):
        authenticated_profile_uuid = ""
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user=user)
            authenticated_profile_uuid = profile.uuid

        try:
            certificate = Certificate.objects.get(uuid=id)
        except Certificate.DoesNotExist:
            return JsonResponse(
                status=status.HTTP_404_NOT_FOUND,
                data={},
            )

        data = CertificateInfoSerializer(instance=certificate).data

        if str(certificate.student.profile.uuid) == str(authenticated_profile_uuid):
            data["authorized"] = True

        return JsonResponse(status=status.HTTP_200_OK, data=data)
