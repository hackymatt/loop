from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from mailer.mailer import Mailer
from django.conf import settings


class ContactViewSet(ViewSet):
    http_method_names = ["post"]

    def contact(self, request):
        contact_data = request.data

        full_name = contact_data["full_name"]
        email = contact_data["email"]
        subject = contact_data["subject"]
        message = contact_data["message"]

        mailer = Mailer()
        data = {
            **{
                "full_name": full_name,
                "email": email,
                "subject": subject,
                "message": message,
            }
        }
        mailer.send(
            email_template="contact.html",
            to=[settings.ADMIN_EMAIL],
            subject="Nowa wiadomość ze strony.",
            data=data,
        )

        return Response(status=status.HTTP_200_OK, data=contact_data)
