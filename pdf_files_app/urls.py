from django.urls import path
from .views import CreateListPDFView, DeletePDFView, DeleteAllPDFView

urlpatterns = [
    path('pdfs/', CreateListPDFView.as_view()),
    path('pdfs/<int:pk>/', DeletePDFView.as_view()),
    path('pdfs/create/', DeletePDFView.as_view()),
    path('pdfs/delete/', DeleteAllPDFView.as_view()),
]