from rest_framework.serializers import Serializer, IntegerField, FloatField


class EarningSerializer(Serializer):
    month = IntegerField()
    year = IntegerField()
    hours = FloatField()
    price = FloatField()
    rate = FloatField()
    commission = IntegerField()
    # total = DecimalField(max_digits=7, decimal_places=2)