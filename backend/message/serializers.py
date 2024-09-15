from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
    ImageField,
    UUIDField,
)
from message.models import Message
from profile.models import Profile


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

    def update(self, instance, validated_data):
        status = validated_data.pop("get_status_display", instance.status)

        Message.objects.filter(pk=instance.pk).update(**validated_data, status=status)
        instance = Message.objects.get(pk=instance.pk)

        return instance


class MessageSerializer(ModelSerializer):
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

        return obj

    def update(self, instance, validated_data):
        status = validated_data.pop("get_status_display", instance.status)

        Message.objects.filter(pk=instance.pk).update(**validated_data, status=status)
        instance = Message.objects.get(pk=instance.pk)

        return instance
