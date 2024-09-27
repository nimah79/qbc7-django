from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from .models import Artist
from .serializers import ArtistSerializer


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
    ]

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
