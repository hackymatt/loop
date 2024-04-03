from rest_framework.serializers import ModelSerializer
from finance.models import Finance, FinanceHistory


class FinanceSerializer(ModelSerializer):
    class Meta:
        model = Finance
        exclude = (
            "id",
            "modified_at",
            "created_at",
            "lecturer",
        )

    def update(self, instance, validated_data):
        validated_data.pop("rate")
        validated_data.pop("commission")
        account = validated_data.pop("account")
        current_account = instance.account

        if current_account != account:
            FinanceHistory.objects.create(
                lecturer=instance.lecturer,
                account=current_account,
                rate=instance.rate,
                commission=instance.commission,
            )

        instance.account = account
        instance.save()

        return instance
