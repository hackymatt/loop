from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from module.serializers import ModuleSerializer, ModuleGetSerializer
from module.filters import ModuleFilter
from module.models import Module


class ModuleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminUser]
    filterset_class = ModuleFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ModuleGetSerializer
        elif self.action == "retrieve":
            return ModuleGetSerializer
        else:
            return self.serializer_class
