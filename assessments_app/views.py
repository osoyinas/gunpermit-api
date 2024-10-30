from django.utils import timezone
from auth_app.generics import *
from assessments_app.models import AssessmentModel, PlaceModel
from assessments_app.serializers import AssessmentSerializer, PlaceSerializer
from auth_app.permissions import IsAdminOrReadOnly


class ListCreatePlace (ReadableListCreateAPIView):
    queryset = PlaceModel.objects.all()
    serializer_class = PlaceSerializer


class ListCreateAssessment(ReadableListCreateAPIView):
    queryset = AssessmentModel.objects.all()
    serializer_class = AssessmentSerializer


class RetrieveUpdateDestroyAssessment(ReadableRetrieveUpdateDestroyAPIView):
    queryset = AssessmentModel.objects.all()
    serializer_class = AssessmentSerializer


class NextAssessmentByPlace(ReadableRetrieveAPIView):
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        place_id = self.kwargs.get('pk')
        return AssessmentModel.objects.filter(place_id=place_id, date__gte=timezone.now()).order_by('date')

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()
