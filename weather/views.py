# @package weather.views
#
# Views data controls for weather rest API View
# @author Pablo Donaire (pdonaire1 at gmail.com)
# @version 1.0.0
import json 

from rest_framework import (
    permissions, viewsets
)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from .models import (
    Weather, WeatherJournal
)
from .utils import obtainWindSpeed
from .serializers import WeatherJournalSerializer, WeatherSerializer
from rest_framework.pagination import PageNumberPagination

class WeatherApiView(APIView):
    """
    View to list all Weather in the system.

    * All users are able to access this view.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """
        Return a list of all Weather.
        """
        response = obtainWindSpeed(Weather, cities=True)

        return Response(json.loads(response))

class WeatherJournalListView(ListAPIView):
    queryset = Weather.objects.all().order_by('-date_register')
    serializer_class = WeatherSerializer
    pagination_class = PageNumberPagination

class WeatherJournalViewset(viewsets.ModelViewSet):
    """
    """
    queryset = WeatherJournal.objects.all()
    serializer_class = WeatherJournalSerializer
    permission_classes = [permissions.AllowAny]


