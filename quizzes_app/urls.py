from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RetrieveDestroyQuizAPIView, CreateQuizAPIView


urlpatterns = [
    path('', CreateQuizAPIView.as_view(), name='create-quiz'),
    path('<int:pk>/', RetrieveDestroyQuizAPIView.as_view(),
         name='retrieve-destroy-quiz'),
]
