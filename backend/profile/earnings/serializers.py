from rest_framework.serializers import (
    Serializer,
    IntegerField,
    FloatField,
    BooleanField,
)


class LecturerEarningSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    earnings = FloatField(source="cost")


class AdminEarningSerializer(Serializer):
    actual = BooleanField()
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()
