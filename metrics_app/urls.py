from django.urls import path

from metrics_app.views import ListTopicResults, ListUserResults, UserQuestionAttemptsView


urlpatterns = [
    path('results', ListUserResults.as_view(), name='results'),
    path('results/topics/', ListTopicResults.as_view(), name='topic_results'),
    path('results/topics/count/', UserQuestionAttemptsView.as_view(), name='user_question_attempts'),
]
