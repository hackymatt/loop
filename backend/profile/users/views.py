from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from profile.users.serializers import UserSerializer
from profile.models import Profile
from profile.users.filters import UserFilter


class UserViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Profile.objects.all().order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated, IsAdminUser]
