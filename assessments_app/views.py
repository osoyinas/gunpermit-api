from datetime import timezone
from rest_framework import generics, parsers

from assessments_app.models import AssessmentModel
from assessments_app.serializers import AssessmentSerializer
from auth_app.permissions import IsAdminOrReadOnly

# Create your views here.
class ListCreateAssessment(generics.ListCreateAPIView):
    queryset = AssessmentModel.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class RetrieveUpdateDestroyAssessment(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssessmentModel.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class NextAssessmentByPlace(generics.RetrieveAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        place_id = self.kwargs['pk']
        return AssessmentModel.objects.filter(place_id=place_id, date__gte=timezone.now()).order_by('date')\
            
    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()