from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import WeatherApiView

urlpatterns = [
    path('weather/', WeatherApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)