from rest_framework import serializers

from quizzes_app.models import QuizResultModel


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResultModel
        fields = ('id', 'created_at', 'score', 'passed')
