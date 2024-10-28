from rest_framework import serializers

from metrics_app.models import TopicMetricsModel
from tracking_app.models import QuizResultModel


class ResultsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', read_only=True)
    score = serializers.CharField(source='score_str', read_only=True)
    mark = serializers.IntegerField(source='score', read_only=True)

    class Meta:
        model = QuizResultModel
        fields = ('id', 'date', 'score', 'mark', 'passed')


class TopicMetricsSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source='topic.title')

    class Meta:
        model = TopicMetricsModel
        fields = ('topic', 'mark', 'full_mark')
