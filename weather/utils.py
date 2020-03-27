# @package weather.utils
#
# utility script for weather package
# @author Pablo Donaire (pdonaire1 at gmail.com)
# @date 25-03-2020
# @version 1.0.0

import json
import requests

from django.utils import timezone

from rest_framework.pagination import PageNumberPagination

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from .models import WeatherJournal
from .serializers import WeatherJournalSerializer

URL_API_WIND = 'https://app.deta.sh/hw6g4zdvlmao/'
URL_API_CITIES = 'https://app.deta.sh/hw6g4zdvlmao/lookup?'

class WeatherUtils():
    def getCityName(self, coord_char):
        return requests.get(
            URL_API_CITIES + coord_char[0] + '&' + coord_char[1],
            verify=True
        ).json()

    def coordinatesToJson(self, coordinates):
        dict_coordinates = {}
        for digit in coordinates:
            value_coord = digit[:-1].strip()
            coord = digit[-1:].lower()
            dict_coordinates[coord] = value_coord
        return dict_coordinates

    def obtainWindSpeed(self, model, cities=False):
        """!
        function to get the api data app.deta.sh

        @param cities true or false value to get cities

        @return object json with the following structure
            example:
                [
                    {
                        "city": "London, United Kingdom", 
                        "wind_speed": "13 kph", 
                        "coordinates": { 
                        "w": "0.1278",
                        "n": "51.5074"
                        }
                    }, ...
                ]
        """
        response = requests.get(URL_API_WIND, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.table('tr')
        data = []
        for row in rows[1:]:
            column = row('td')
            td_elements = [c.text.replace('°', '') for c in column]
            coordinates = td_elements[0].split(',')
            coordinates = ["=".join(coordinate.strip().split(" ")[::-1]).lower() for coordinate in coordinates]
            wind_speed = td_elements[1]
            dict_coordinates = self.coordinatesToJson(coordinates)

            if cities:
                response_cities = self.getCityName(coordinates)
                city = response_cities['result'] if response_cities.get('result', None) else None
            else:
                city = None
            object_model = model.objects.filter(city=city, wind_speed=wind_speed).last()
            if object_model:
                date_now = timezone.now()
                diff = relativedelta(date_now, object_model.date_register)
                if diff.hours >= 1:
                    object_model = model.objects.create(
                        city=city,
                        coordinates=dict_coordinates,
                        wind_speed=wind_speed
                    )
            else:
                object_model = model.objects.create(
                    city=city,
                    coordinates=dict_coordinates,
                    wind_speed=wind_speed
                )
            comments = WeatherJournal.objects.filter(fk_weather=object_model.pk)
            data.append({
                'id': object_model.pk,
                'coordinates': dict_coordinates,
                'wind_speed': wind_speed,
                'city': city,
                'comments': WeatherJournalSerializer(comments, many=True).data})
            dict_coordinates = {}
        return json.dumps(data)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'
