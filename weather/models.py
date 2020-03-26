# @package weather.models
#
# Data model for weather storage
# @author Pablo Donaire (pdonaire1 at gmail.com)
# @version 1.0.0
from django.contrib.postgres.fields import JSONField
from django.db import models


class Weather(models.Model):
    """
    Class to store Weather information
    """
    city = models.CharField(max_length=50)
    coordinates = JSONField()
    wind_speed = models.CharField(max_length=50)
    date_register = models.DateTimeField(auto_now_add=True)

    class Meta:
        """!
        Meta data class
        """
        ordering = ('pk',)
        verbose_name = 'Weather'
        db_table = 'weather'

    def __str__(self):
        """!
        Serialization method
        """
        return self.city


class WeatherJournal(models.Model):
    """
    Class to store WeatherJournal information
    """
    fk_weather = models.ForeignKey(Weather, on_delete=models.DO_NOTHING)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        """!
        Meta data class
        """
        ordering = ('pk',)
        verbose_name = 'WeatherJournal'
        db_table = 'weather_journal'

    def __str__(self):
        """!
        Serialization method
        """
        return self.comment