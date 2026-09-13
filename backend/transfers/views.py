from rest_framework import generics

from .models import Club, Player, TransferRumour
from .serializers import (
    ClubSerializer,
    PlayerSerializer,
    TransferRumourSerializer,
)


class ClubListCreateView(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class PlayerListCreateView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TransferRumourListCreateView(generics.ListCreateAPIView):
    serializer_class = TransferRumourSerializer

    def get_queryset(self):
        queryset = TransferRumour.objects.all().order_by("-created_at")

        player_id = self.request.query_params.get("player")

        if player_id:
            queryset = queryset.filter(player_id=player_id)

        return queryset


class TransferRumourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRumour.objects.all()
    serializer_class = TransferRumourSerializer

def get_queryset(self):
    queryset = TransferRumour.objects.all().order_by("-created_at")

    player_id = self.request.query_params.get("player")
    probability = self.request.query_params.get("probability")

    if player_id:
        queryset = queryset.filter(player_id=player_id)

    if probability:
        queryset = queryset.filter(probability=probability)

    return queryset