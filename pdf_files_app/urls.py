from django.urls import path
from .views import CreateListPDFView, DeletePDFView, DeleteAllPDFView

urlpatterns = [
    path('', CreateListPDFView.as_view()),
    path('<int:pk>/', DeletePDFView.as_view()),
    path('create/', DeletePDFView.as_view()),
    path('delete/', DeleteAllPDFView.as_view()),
]