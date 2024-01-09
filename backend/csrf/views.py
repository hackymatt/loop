from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token

class CsrfViewSet(ViewSet):
    http_method_names = ["get"]
    def get_csrf(self, request):
        return Response(status=status.HTTP_200_OK,
                data={'csrf_token': get_token(request)})