from django.forms import ValidationError
from rest_framework import serializers

from questions_app.serializers import QuestionSerializer
from quizzes_app.mocks import createQuizMock
from .models import QuizModel, QuizQuestionModel
from questions_app.models import QuestionModel


class QuizQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuizQuestionModel
        fields = ['question']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(
        source='quizquestionmodel_set',
        many=True)

    class Meta:
        model = QuizModel
        fields = ['id',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'questions']

class QuizCreateSerializer(serializers.ModelSerializer):
    questions = serializers.ListField(
        child=serializers.IntegerField()
    )

    class Meta:
        model = QuizModel
        fields = ['title', 'description', 'questions']

    def create(self, validated_data):
        question_ids = validated_data.pop('questions')
        
        # Verificar que todas las preguntas existan
        questions = QuestionModel.objects.filter(id__in=question_ids)
        if len(questions) != len(question_ids):
            raise serializers.ValidationError("Una o más preguntas no existen.")
        
        # Crear el quiz
        quiz = QuizModel.objects.create(**validated_data)
        
        # Asociar las preguntas con el quiz
        for question in questions:
            QuizQuestionModel.objects.create(quiz=quiz, question=question)
        
        return quiz