from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MakeQuizAPIView, RetrieveDestroyQuizAPIView, CreateQuizAPIView


urlpatterns = [
    path('', CreateQuizAPIView.as_view(), name='create-quiz'),
    path('<int:pk>/', RetrieveDestroyQuizAPIView.as_view(),
         name='retrieve-destroy-quiz'),
    path('<int:pk>/make/', MakeQuizAPIView.as_view(), name='make-quiz'),
]
