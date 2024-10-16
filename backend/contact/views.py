from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from mailer.mailer import Mailer
from config_global import CONTACT_EMAIL


class ContactAPIView(APIView):
    """API View for handling contact form submissions."""

    def post(self, request):
        """Handles incoming contact form submissions."""
        contact_data = request.data

        full_name = contact_data["full_name"]
        email = contact_data["email"]
        subject = contact_data["subject"]
        message = contact_data["message"]

        # Send email using the Mailer
        mailer = Mailer()
        data = {
            "full_name": full_name,
            "email": email,
            "subject": subject,
            "message": message,
        }

        mailer.send(
            email_template="contact.html",
            to=[CONTACT_EMAIL],
            subject="Nowa wiadomość ze strony",
            data=data,
        )

        return Response(status=status.HTTP_200_OK, data=contact_data)
