from assessments_app.models import AssessmentModel
from rest_framework import serializers


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentModel
        fields = '__all__'