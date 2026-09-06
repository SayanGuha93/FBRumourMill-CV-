from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Club
from .serializers import ClubSerializer


@api_view(['GET'])
def club_list(request):
    clubs = Club.objects.all()
    serializer = ClubSerializer(clubs, many=True)

    return Response(serializer.data)