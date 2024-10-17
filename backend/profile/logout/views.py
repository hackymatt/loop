from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.logout.serializers import ProfileLogoutSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout


class ProfileLogoutViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = ProfileLogoutSerializer

    def create(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK, data={})
