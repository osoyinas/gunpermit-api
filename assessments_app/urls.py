from django.urls import path

from assessments_app.views import ListCreateAssessment, RetrieveUpdateDestroyAssessment



urlpatterns = [
    path('', ListCreateAssessment.as_view(), name='list_create_assessment'),
    path('<int:pk>/', RetrieveUpdateDestroyAssessment.as_view(), name='retrieve_update_destroy_assessment'),
    path('next/<int:pk>', RetrieveUpdateDestroyAssessment.as_view(), name='next_assessment'),
]
