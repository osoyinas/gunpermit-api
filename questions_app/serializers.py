from rest_framework import serializers
from .models import TopicModel, QuestionModel 

ANSWERS_STRUCTURE = [{'answer': str, 'is_true': bool}] * 3
DEFAULT_ANSWERS = [{'answer': "respuesta", 'is_true': False}] * 3

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField()
    class Meta:
        model = QuestionModel
        fields = ['id','topic', 'question', 'answers']


class TopicSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = TopicModel
        fields = ['id', 'name', 'questions']
    
    




