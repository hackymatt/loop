from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsLecturer
from finance.serializers import FinanceSerializer
from finance.models import Finance
from profile.models import Profile


class FinanceDetailsViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = [IsAuthenticated, IsLecturer]

    def list(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        finance = Finance.objects.filter(lecturer=profile).first()

        serializer = FinanceSerializer(finance, context={"request": request})

        return Response(serializer.data)

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return Finance.objects.filter(lecturer=profile).first()
