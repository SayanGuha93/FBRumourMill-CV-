from rest_framework import serializers
from .models import Rumour


class RumourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rumour
        fields = "__all__"