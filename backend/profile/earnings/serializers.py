from rest_framework.serializers import Serializer, IntegerField, FloatField, CharField


class LecturerEarningSerializer(Serializer):
    year = IntegerField()
    month = IntegerField()
    earnings = FloatField(source="cost")


class AdminEarningSerializer(Serializer):
    year = IntegerField()
    month = IntegerField()
    cost = FloatField()
    profit = FloatField()
