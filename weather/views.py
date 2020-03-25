# @package weather.views
#
# Views data controls for weather rest API View
# @author Pablo Donaire (pdonaire1 at gmail.com)
# @version 1.0.0
import json 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .utils import obtainWindSpeed

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
        response = obtainWindSpeed(cities=True)

        return Response(json.loads(response))

