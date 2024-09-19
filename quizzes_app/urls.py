from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RetrieveQuiz


urlpatterns = [
    path('<int:pk>/', RetrieveQuiz.as_view(), name='retrieve_quiz'),
]
