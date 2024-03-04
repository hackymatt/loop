from rest_framework.serializers import ModelSerializer
from finance.models import Finance


class FinanceSerializer(ModelSerializer):
    class Meta:
        model = Finance
        fields = ("account",)
