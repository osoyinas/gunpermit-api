from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListTopicsView, RetrieveUpdateDestroyTopicsView, ListQuestionsTopicView, ListQuestionsView, RetrieveDestroyUpdateQuestionView


urlpatterns = [
    path('topics/', ListTopicsView.as_view(), name='list_create_topics'),
    path('topics/<int:pk>/', RetrieveUpdateDestroyTopicsView.as_view(),
         name='retrieve_topics'),
    path('topics/<int:topic_id>/questions/',
         ListQuestionsTopicView.as_view(), name='list_questions_topic'),
    path('questions/', ListQuestionsView.as_view(),
         name='list_create_questions'),
    path('questions/<int:pk>/', RetrieveDestroyUpdateQuestionView.as_view(),
         name='retrieve_destroy_update_question'),
]
