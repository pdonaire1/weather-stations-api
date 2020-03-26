from django.contrib import admin
from .models import Weather, WeatherJournal

admin.site.register(Weather)
admin.site.register(WeatherJournal)