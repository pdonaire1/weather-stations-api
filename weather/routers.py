from rest_framework import routers

from .views import WeatherJournalViewset

router = routers.DefaultRouter()

router.register(r'weather-observations', WeatherJournalViewset)