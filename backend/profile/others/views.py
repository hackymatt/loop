from rest_framework.viewsets import ModelViewSet
from profile.others.serializers import OtherSerializer
from profile.others.filters import OtherFilter
from profile.models import OtherProfile
from config_global import DUMMY_OTHER_EMAIL


class OtherViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        OtherProfile.objects.exclude(profile__user__email=DUMMY_OTHER_EMAIL)
        .add_full_name()
        .order_by("id")
    )
    serializer_class = OtherSerializer
    filterset_class = OtherFilter
    search_fields = [
        "profile__user__first_name",
        "profile__user__last_name",
        "profile__user__email",
    ]
