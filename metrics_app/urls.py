from django.urls import path

from metrics_app.views import ListTopicResults, ListUserResults


urlpatterns = [
    path('results', ListUserResults.as_view(), name='results'),
    path('results/topics/', ListTopicResults.as_view(), name='topic_results'),
]
