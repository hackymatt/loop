from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from course.serializers import CourseSerializer
from course.models import Course


class CourseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        if self.get_object().active:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"course": "Kurs jest aktywny."},
            )

        return super().destroy(request, *args, **kwargs)
