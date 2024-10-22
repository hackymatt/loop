from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mailer.mailer import Mailer
from django.views.decorators.csrf import csrf_exempt
from config_global import CONTACT_EMAIL


class ContactAPIView(APIView):
    http_method_names = ["post"]

    @csrf_exempt
    def post(self, request):
        contact_data = request.data

        mailer = Mailer()
        mailer.send(
            email_template="contact.html",
            to=[CONTACT_EMAIL],
            subject="Nowa wiadomość ze strony",
            data=contact_data,
        )

        return Response(status=status.HTTP_200_OK, data=contact_data)
