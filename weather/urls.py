from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import WeatherApiView, WeatherJournalListView

urlpatterns = [
    path('weather/', WeatherApiView.as_view()),
    path('weather-journal/', WeatherJournalListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)