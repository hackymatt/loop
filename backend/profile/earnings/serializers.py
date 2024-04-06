from rest_framework.serializers import (
    Serializer,
    IntegerField,
    FloatField,
    DateTimeField,
)


class LecturerEarningSerializer(Serializer):
    billing_date = DateTimeField()
    year = IntegerField()
    month = IntegerField()
    earnings = FloatField(source="cost")


class AdminEarningSerializer(Serializer):
    billing_date = DateTimeField()
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()
