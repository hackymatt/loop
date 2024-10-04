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
from urllib.parse import quote_plus


class ProfileSerializer(ModelSerializer):
    id = UUIDField(source="uuid")
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="get_gender_display")
    image = ImageField()
    user_type = CharField(source="get_user_type_display")

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
            "user_type",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


class MessageGetSerializer(ModelSerializer):
    sender = ProfileSerializer()
    recipient = ProfileSerializer()
    status = CharField(source="get_status_display")

    class Meta:
        model = Message
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    status = CharField(source="get_status_display")
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
        status = validated_data.pop("get_status_display")
        recipient_id = validated_data.pop("recipient_id", None)
        recipient_uuid = validated_data.pop("recipient_uuid", None)
        recipient_type = validated_data.pop("recipient_type", None)

        user = self.context["request"].user
        sender = Profile.objects.get(user=user)

        if recipient_id:
            if recipient_type[0] == "S":
                recipient = StudentProfile.objects.get(pk=recipient_id).profile
            elif recipient_type[0] == "W":
                recipient = LecturerProfile.objects.get(pk=recipient_id).profile
            else:
                recipient = AdminProfile.objects.get(pk=recipient_id).profile
        else:
            recipient = Profile.objects.get(uuid=recipient_uuid)

        obj, _ = Message.objects.get_or_create(
            sender=sender, recipient=recipient, status=status, **validated_data
        )

        notify(
            profile=obj.recipient,
            title="Otrzymano nową wiadomość",
            subtitle=obj.subject,
            description=obj.body,
            path=f"/account/messages?sort_by=-created_at&page_size=10&type=INBOX&search={quote_plus(obj.subject)}",
            icon="mdi:email",
        )

        mailer = Mailer()
        data = {
            **{
                "full_name": f"{sender.user.first_name} {sender.user.last_name}",
                "subject": obj.subject,
                "message": obj.body,
            }
        }
        mailer.send(
            email_template="message.html",
            to=[obj.recipient.user.email],
            subject="Nowa wiadomość",
            data=data,
        )

        return obj

    def update(self, instance, validated_data):
        status = validated_data.pop("get_status_display", instance.status)

        Message.objects.filter(pk=instance.pk).update(**validated_data, status=status)
        instance = Message.objects.get(pk=instance.pk)

        return instance
