from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListCreateTopicsView, RetrieveTopicsView, ListQuestionsTopicView, ListCreateQuestionsView


urlpatterns = [
    path('topics/',ListCreateTopicsView.as_view()),
    path('topics/<int:pk>', RetrieveTopicsView.as_view()),
    path('topics/<int:topic_id>/questions/', ListQuestionsTopicView.as_view()),
    path('questions/', ListCreateQuestionsView.as_view()),
    ]