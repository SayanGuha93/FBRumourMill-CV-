from rest_framework import serializers
from .models import Club, Player, TransferRumour


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(min_value=15, max_value=50)

    class Meta:
        model = Player
        fields = '__all__'


class TransferRumourSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRumour
        fields = '__all__'