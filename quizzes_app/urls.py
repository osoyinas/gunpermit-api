from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ListQuizCategoriesView, MakeQuizAPIView, RetrieveDestroyUpdateQuizAPIView, ListCreateQuizApiView


urlpatterns = [
    path('', ListCreateQuizApiView.as_view(), name='list-create-quiz'),
    path('<int:pk>/', RetrieveDestroyUpdateQuizAPIView.as_view(),
         name='retrieve-destroy-quiz'),
    path('<int:pk>/make/', MakeQuizAPIView.as_view(), name='make-quiz'),
    path('categories/', ListQuizCategoriesView.as_view(), name='list-quiz-categories'),
]
