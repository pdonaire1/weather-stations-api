from django.test import TestCase
from rest_framework.test import APIClient

from .models import (
    Weather, WeatherJournal
)


class WeatherApiTest(TestCase):
    """
    Class to test the enpoint that controls the communication to the apis
    """
    def setUp(self):
        """
        Method to configure initial values ​​of
        the unit test
        """
        self.client = APIClient()

    def test_get(self):
        """
        Method to test the listing of the weather taken from the apis
        """
        response = self.client.get('/weather/', format="json")
        self.assertEqual(response.status_code, 200)


class WeatherJournalTest(TestCase):
    """
    Class to test the weather comments enpoint
    """

    def setUp(self):
        """
        Method to configure initial values ​​of
        the unit test
        """
        self.client = APIClient()
        self.weather = Weather.objects.create(
            city='London, United Kingdom',
            coordinates={
                    "n": "51.5074",
                    "w": "0.1278"
                },
            wind_speed='19 kph'
        )
        self.weather_journal = WeatherJournal.objects.create(
            fk_weather=self.weather,
            comment="New comment"
        )

    def test_list(self):
        """
        Method to test the listing of the weather comment
        """
        response = self.client.get('/weather-observations/', format="json")
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        """
        Method to test the creating of the weather comment
        """
        param = {
            "comment": "New Commnet create",
            "fk_weather_id": self.weather.pk
        }
        response = self.client.post(
            '/weather-observations/',
            param,
            format="json"
        )
        self.assertEqual(response.status_code, 201)
