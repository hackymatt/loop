from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User


class ProfileUnregisterViewSet(ModelViewSet):
    http_method_names = ["delete"]
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.delete()

        return Response({})
