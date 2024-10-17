from assessments_app.models import AssessmentModel, PlaceModel
from rest_framework import serializers

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceModel
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentModel
        fields = '__all__'