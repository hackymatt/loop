from rest_framework.viewsets import ModelViewSet
from technology.serializers import (
    TechnologyListSerializer,
)
from technology.filters import (
    TechnologyFilter,
)
from technology.models import (
    Technology,
)


class TechnologyViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Technology.objects.all()
    serializer_class = TechnologyListSerializer
    filterset_class = TechnologyFilter
