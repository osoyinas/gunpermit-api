from rest_framework import serializers

from questions_app.serializers import QuestionSerializer
from .models import QuizModel, QuizQuestion


class QuizQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuizQuestion
        fields = ['question', 'order']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, required=False)

    class Meta:
        model = QuizModel
        fields = ['id', 'title', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        test = QuizModel.objects.create(**validated_data)
        for question_data in questions_data:
            QuizQuestion.objects.create(test=test, **question_data)
        return test

    def update(self, instance, validated_data):

        return instance
