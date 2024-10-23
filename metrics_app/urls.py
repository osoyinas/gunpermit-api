from django.urls import path

from metrics_app.views import ListUserResults


urlpatterns = [
    path('results/', ListUserResults.as_view(), name='results'),
]
