from rest_framework.serializers import Serializer, IntegerField, FloatField, CharField


class EarningSerializer(Serializer):
    year = IntegerField()
    month = IntegerField()   
    earnings = FloatField()
