# @package weather.serializer
#
# data serializer package for weather app
# @author Pablo Donaire (pdonaire1 at gmail.com)
# @version 1.0.0
from rest_framework import serializers

from .models import (
    Weather, WeatherJournal
)

class WeatherSerializer(serializers.ModelSerializer):
    """
    """
    comments = serializers.SerializerMethodField('weather_comments')

    def weather_comments(self, instance):
        try:
            queryset = WeatherJournal.objects.filter(fk_weather=instance.pk)
            return WeatherCommentsSerializer(queryset, many=True).data
        except:
            return []

    class Meta:
    
        model = Weather
        fields = (
            'city', 'coordinates',
            'wind_speed', 'date_register',
            'comments'
        )

class WeatherCommentsSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
    
        model = WeatherJournal
        fields = ('comment', 'time')
        read_only_fields = ('time',)

class WeatherJournalSerializer(serializers.ModelSerializer):
    """
    """
    fk_weather = WeatherSerializer(many=False, read_only=True)
    try:
        queryset = Weather.objects.select_related().values_list(
                                                    'pk',
                                                    'city'
                                                  )
        fk_weather_id = serializers.ChoiceField(
            write_only=True,
            choices=queryset,
            required=False,
            allow_null=True
        )
    except:
        fk_weather_id = serializers.CharField(write_only=True)
        pass

    class Meta:
    
        model = WeatherJournal
        fields = (
            'comment', 'time',
            'fk_weather', 'fk_weather_id',
        )
        read_only_fields = ('time',)
