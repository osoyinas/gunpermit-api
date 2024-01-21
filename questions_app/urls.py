from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreateTopicsView, RetrieveUpdateDestroyTopicsView, ListQuestionsTopicView, ListCreateQuestionsView, DestroyUpdateQuestionView


urlpatterns = [
    path('topics/',ListCreateTopicsView.as_view(), name='list_create_topics'),
    path('topics/<int:pk>', RetrieveUpdateDestroyTopicsView.as_view(), name='retrieve_topics'),
    path('topics/<int:topic_id>/questions/', ListQuestionsTopicView.as_view(), name='list_questions_topic'),
    path('questions/', ListCreateQuestionsView.as_view(), name='list_create_questions'),
    path('questions/<int:pk>', DestroyUpdateQuestionView.as_view(), name='destroy_update_question'),
    ]