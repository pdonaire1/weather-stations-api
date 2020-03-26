# @package weather.utils
#
# utility script for weather package
# @author Pablo Donaire (pdonaire1 at gmail.com)
# @date 25-03-2020
# @version 1.0.0

import json
import requests

from django.utils import timezone

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

URL_API_WIND = 'https://app.deta.sh/hw6g4zdvlmao/'
URL_API_CITIES = 'https://app.deta.sh/hw6g4zdvlmao/lookup?'

def obtainWindSpeed(model, cities=False):
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
        wind_speed = td_elements[1]
        dict_coordinates = {}
        control = 0
        for digit in coordinates:
            value_coord = digit[:-1].strip()
            coord = digit[-1:].lower()
            dict_coordinates[coord] = value_coord
            control += 1
            if control == 2:
                if cities:
                    coord_char = [key + '=' + str(value) for key, value in dict_coordinates.items()]
                    response_cities = response = requests.get(
                        URL_API_CITIES + coord_char[0] + '&' + coord_char[1],
                        verify=True
                    ).json()
                    if response_cities.get('result', None):
                        city = response_cities['result']
                    else:
                        city = None
                else:
                    city = None
                object_model = model.objects.filter(city=city, wind_speed=wind_speed).last()
                if object_model:
                    date_now = timezone.now()
                    diff = relativedelta(date_now, object_model.date_register)
                    if diff.hours >= 1:
                        print(city, dict_coordinates, wind_speed)
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
                data.append({'id': object_model.pk, 'coordinates': dict_coordinates, 'wind_speed': wind_speed, 'city': city})
                dict_coordinates = {}
                control = 0
        
    return json.dumps(data)
