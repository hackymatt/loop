from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from module.serializers import ModuleSerializer, ModuleGetSerializer
from module.filters import ModuleFilter
from module.models import Module


class ModuleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Module.objects.prefetch_related("lessons").all().order_by("id")
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminUser]
    filterset_class = ModuleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ModuleGetSerializer
        return self.serializer_class

    def get_queryset(self):
        sort_by = self.request.query_params.get("sort_by", None)
        if sort_by:
            if "lessons_count" in sort_by:
                return self.queryset.add_lessons_count()

        return self.queryset
