from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RetrieveDestroyAPIView


urlpatterns = [
    path('<int:pk>/', RetrieveDestroyAPIView.as_view(), name='retrieve-destroy-quiz'),
]
