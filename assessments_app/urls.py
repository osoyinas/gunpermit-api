from django.urls import path

from assessments_app.views import ListCreateAssessment, ListCreatePlace, RetrieveUpdateDestroyAssessment



urlpatterns = [
    path('places/', ListCreatePlace.as_view(), name='list_create_place'),
    path('assessments/', ListCreateAssessment.as_view(), name='list_create_assessment'),
    path('assessments/<int:pk>/', RetrieveUpdateDestroyAssessment.as_view(), name='retrieve_update_destroy_assessment'),
    path('assessments/next/<int:pk>', RetrieveUpdateDestroyAssessment.as_view(), name='next_assessment'),
]
