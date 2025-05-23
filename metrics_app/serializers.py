from rest_framework import serializers

from tracking_app.models import QuizResultModel

class ResultsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', read_only=True)
    score = serializers.CharField(source='score_str', read_only=True)
    mark = serializers.IntegerField(source='score', read_only=True)
    quiz = serializers.CharField(source='quiz.title', read_only=True)
    category = serializers.CharField(source='quiz.category.title', read_only=True)
    class Meta:
        model = QuizResultModel
        fields = ('id', 'date', 'score', 'mark', 'passed', 'quiz', 'category')


class TopicDataSerializer(serializers.Serializer):
    answered = serializers.IntegerField()
    total = serializers.IntegerField()
    correct = serializers.IntegerField()
    incorrect = serializers.IntegerField()

class UserQuestionAttemptsResponseSerializer(serializers.Serializer):
    topics = serializers.DictField(child=TopicDataSerializer())
    answered = serializers.IntegerField()
    correct = serializers.IntegerField()
    incorrect = serializers.IntegerField()
    total = serializers.IntegerField()
