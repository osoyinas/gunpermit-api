from django.urls import path

from assessments_app.views import ListCreateAssessment, ListCreatePlace, RetrieveUpdateDestroyAssessment, NextAssessmentByPlace



urlpatterns = [
    path('places/', ListCreatePlace.as_view(), name='list_create_place'),
    path('places/<int:pk>/next-assessment/', NextAssessmentByPlace.as_view(), name='next_assessment'),
    path('assessments/', ListCreateAssessment.as_view(), name='list_create_assessment'),
    path('assessments/<int:pk>/', RetrieveUpdateDestroyAssessment.as_view(), name='retrieve_update_destroy_assessment'),
]
