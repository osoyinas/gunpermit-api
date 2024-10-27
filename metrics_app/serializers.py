from rest_framework import serializers

from tracking_app.models import QuizResultModel


class ResultsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', read_only=True)
    score = serializers.CharField(source='score_str', read_only=True)
    mark = serializers.IntegerField(source='score', read_only=True)

    class Meta:
        model = QuizResultModel
        fields = ('id', 'date', 'score', 'mark', 'passed')


class TopicResultSerializer(serializers.Serializer):
    topic = serializers.CharField()
    mark = serializers.IntegerField()
    full_mark = serializers.IntegerField()

    class Meta:
        fields = ('topic', 'mark', 'full_mark')


class TopicResultsListSerializer(serializers.ListSerializer):
    child = TopicResultSerializer()
