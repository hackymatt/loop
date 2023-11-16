from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from profile.details.serializers import (
    ProfileDetailsSerializer,
    LecturerDetailsSerializer,
)
from profile.models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist


class ProfileDetailsViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = User.objects.all()
    serializer_class = ProfileDetailsSerializer

    @staticmethod
    def get_profile(user: User):
        return Profile.objects.get(user=user)

    @staticmethod
    def model_field_exists(obj, field):
        try:
            obj._meta.get_field(field)
            return True
        except (AttributeError, FieldDoesNotExist):
            return False

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "Użytkownik niezalogowany."},
            )

        profile = self.get_profile(user)
        if profile.user_type == "S":
            serializer = ProfileDetailsSerializer(profile)
        else:
            serializer = LecturerDetailsSerializer(profile)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"details": "Użytkownik niezalogowany."},
            )
        profile = self.get_profile(user)

        for key, value in request.data.items():
            if not key == "email":
                if self.model_field_exists(profile, key):
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
