from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
    ImageField,
    UUIDField,
    IntegerField,
)
from message.models import Message
from profile.models import Profile, StudentProfile, LecturerProfile, AdminProfile
from notification.utils import notify
from mailer.mailer import Mailer
from const import UserType
from urllib.parse import quote_plus


class ProfileSerializer(ModelSerializer):
    id = UUIDField(source="uuid")
    full_name = SerializerMethodField()
    image = ImageField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
            "user_type",
        )

    def get_full_name(self, profile: Profile):
        return profile.full_name


class MessageGetSerializer(ModelSerializer):
    sender = ProfileSerializer()
    recipient = ProfileSerializer()

    class Meta:
        model = Message
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    recipient_type = CharField(required=False)
    recipient_id = IntegerField(required=False)
    recipient_uuid = UUIDField(required=False)

    class Meta:
        model = Message
        exclude = (
            "sender",
            "recipient",
        )

    def create(self, validated_data):
        recipient_id = validated_data.pop("recipient_id", None)
        recipient_uuid = validated_data.pop("recipient_uuid", None)
        recipient_type = validated_data.pop("recipient_type", None)

        user = self.context["request"].user
        sender = Profile.objects.get(user=user)

        recipient = self.get_recipient(recipient_id, recipient_uuid, recipient_type)

        message, _ = Message.objects.get_or_create(
            sender=sender, recipient=recipient, **validated_data
        )

        self.notify_recipient(message)

        self.send_email(sender, message)

        return message

    def get_recipient(self, recipient_id, recipient_uuid, recipient_type):
        if recipient_id:
            if recipient_type == UserType.STUDENT:
                return StudentProfile.objects.get(pk=recipient_id).profile
            elif recipient_type == UserType.INSTRUCTOR:
                return LecturerProfile.objects.get(pk=recipient_id).profile
            else:
                return AdminProfile.objects.get(pk=recipient_id).profile
        return Profile.objects.get(uuid=recipient_uuid)

    def notify_recipient(self, message):
        notify(
            profile=message.recipient,
            title="Otrzymano nową wiadomość",
            subtitle=message.subject,
            description=message.body,
            path=f"/account/messages?sort_by=-created_at&page_size=10&type=INBOX&search={quote_plus(message.subject)}",
            icon="mdi:email",
        )

    def send_email(self, sender, message):
        mailer = Mailer()
        data = {
            "full_name": f"{sender.user.first_name} {sender.user.last_name}",
            "subject": message.subject,
            "message": message.body,
        }
        mailer.send(
            email_template="message.html",
            to=[message.recipient.user.email],
            subject="Nowa wiadomość",
            data=data,
        )
