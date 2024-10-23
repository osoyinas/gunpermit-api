from rest_framework import serializers

from quizzes_app.models import QuizResultModel
from rest_framework.fields import CurrentUserDefault


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResultModel
        fields = ('id', 'created_at', 'score', 'passed')


class TopicResultSerializer(serializers.Serializer):
    topic = serializers.CharField()
    mark = serializers.IntegerField()
    full_mark = serializers.IntegerField()

    class Meta:
        fields = ('topic', 'mark', 'full_mark')


class TopicResultsListSerializer(serializers.ListSerializer):
    child = TopicResultSerializer()