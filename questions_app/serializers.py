from rest_framework import serializers
from .models import TopicModel, QuestionModel

ANSWERS_STRUCTURE = [{'answer': str, 'is_true': bool}] * 3
DEFAULT_ANSWERS = [{'answer': "respuesta", 'is_true': False}] * 3


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField()

    class Meta:
        model = QuestionModel
        fields = ['id', 'topic', 'question', 'answers']


class TopicSerializerWithQuestions(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = TopicModel
        fields = ['id', 'title', 'description', 'questions']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicModel
        fields = "__all__"
