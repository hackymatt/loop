from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from profile.users.serializers import UserSerializer, UserFinanceSerializer
from profile.models import Profile
from profile.users.filters import UserFilter
from const import UserType

class UserViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put"]
    queryset = (
        Profile.objects.all().order_by("id")
    )
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserFinanceViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = (
        Profile.objects.filter(user_type=UserType.INSTRUCTOR).add_account().add_rate().add_commission().all().order_by("id")
    )
    serializer_class = UserFinanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]