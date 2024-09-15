from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
    ImageField,
    UUIDField,
)
from message.models import Message
from profile.models import Profile
from notification.utils import notify
from mailer.mailer import Mailer
import urllib.parse


class ProfileSerializer(ModelSerializer):
    id = UUIDField(source="uuid")
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="get_gender_display")
    image = ImageField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
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

    class Meta:
        model = Message
        exclude = ("sender",)

    def create(self, validated_data):
        status = validated_data.pop("get_status_display")
        user = self.context["request"].user
        sender = Profile.objects.get(user=user)

        obj, _ = Message.objects.get_or_create(
            sender=sender, status=status, **validated_data
        )

        notify(
            profile=obj.recipient,
            title="Otrzymano nową wiadomość",
            subtitle=obj.subject,
            description=obj.body,
            path=f"/account/messages?sort_by=-created_at&page_size=10&search={urllib.parse.quote_plus(obj.subject)}",
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
