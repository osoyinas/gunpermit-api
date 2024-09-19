from rest_framework import serializers

from questions_app.serializers import QuestionSerializer
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
