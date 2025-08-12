from django.urls import path

from .views import UpdateStatsView

app_name = 'stats'
urlpatterns = [
    path('', UpdateStatsView.as_view(), name='update-stats'),
]