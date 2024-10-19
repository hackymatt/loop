from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from skill.serializers import SkillSerializer
from skill.filters import SkillFilter
from skill.models import Skill


class SkillViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filterset_class = SkillFilter

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
