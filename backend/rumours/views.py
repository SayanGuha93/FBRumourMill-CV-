from rest_framework import generics
from .models import Rumour
from .serializers import RumourSerializer


class RumourListCreateView(generics.ListCreateAPIView):
    queryset = Rumour.objects.all().order_by("-published_at")
    serializer_class = RumourSerializer


class RumourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rumour.objects.all()
    serializer_class = RumourSerializer