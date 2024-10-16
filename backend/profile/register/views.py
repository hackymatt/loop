from rest_framework.viewsets import ModelViewSet
from profile.register.serializers import ProfileRegisterSerializer
from django.contrib.auth.models import User


class ProfileRegisterViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all().order_by("id")
    serializer_class = ProfileRegisterSerializer
