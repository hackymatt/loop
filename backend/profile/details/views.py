from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.details.serializers import ProfileDetailsSerializer
from django.contrib.auth.models import User


class ProfileDetailsViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = User.objects.all()
    serializer_class = ProfileDetailsSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "Użytkownik niezalogowany."},
            )
        queryset = ProfileDetailsSerializer.get(user)

        serializer = ProfileDetailsSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "Użytkownik niezalogowany."},
            )
        profile = ProfileDetailsSerializer.get(user)

        for key, value in request.data.items():
            if not key == "email":
                if ProfileDetailsSerializer.model_field_exists(profile, key):
                    obj = profile
                else:
                    obj = user
                if value:
                    setattr(obj, key, value)
                else:
                    setattr(obj, key, None)

        user.save()
        profile.save()

        serializer = ProfileDetailsSerializer(profile)
        return Response(serializer.data)
