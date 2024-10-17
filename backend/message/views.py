from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from message.serializers import MessageSerializer, MessageGetSerializer
from message.models import Message
from message.filters import MessageFilter
from profile.models import Profile
from django.db.models import Q, Value


class MessageViewSet(ModelViewSet):
    http_method_names = ["get", "put", "post"]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = MessageFilter
    search_fields = [
        "subject",
        "body",
    ]

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return self.queryset.filter(Q(sender=profile) | Q(recipient=profile)).annotate(
            profile_id=Value(profile.id)
        )

    def get_serializer_class(self):
        if self.action == "list":
            return MessageGetSerializer
        elif self.action == "retrieve":
            return MessageGetSerializer
        else:
            return self.serializer_class
