from django.forms import ValidationError
from rest_framework import serializers

from questions_app.serializers import QuestionSerializer
from quizzes_app.mocks import createQuizMock
from .models import QuizCategoryModel, QuizModel, QuizQuestionModel
from questions_app.models import QuestionModel
from tracking_app.models import UserQuestionAttemptModel, QuizResultModel


class QuizQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='question.id')
    question = serializers.CharField(source='question.question')
    answers = serializers.JSONField(source='question.answers')

    class Meta:
        model = QuizQuestionModel
        fields = ['id', 'question', 'answers']


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


class QuizCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCategoryModel
        fields = "__all__"

class CreateQuizSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError(
                "Una o más preguntas no existen.")

        # Crear el quiz
        quiz = QuizModel.objects.create(**validated_data)

        # Asociar las preguntas con el quiz
        for question in questions:
            QuizQuestionModel.objects.create(quiz=quiz, question=question)

        return quiz

    def to_representation(self, instance):
        attempt = QuizResultModel.objects.filter(
            quiz=instance).order_by('-created_at').first()
        if attempt:
            return {
                'id': instance.id,
                'title': instance.title,
                'description': instance.description,
                'questions': len(instance.questions.all()),
                'score': attempt.score,
                'passed': attempt.passed
            }
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'questions': len(instance.questions.all())
        }


class AnswerItemSerializer(serializers.Serializer):
    question = serializers.IntegerField()  # question ID
    answer = serializers.IntegerField()  # index of the answer


class MakeQuizSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=AnswerItemSerializer()
    )

    def validate(self, attrs):
        quiz = self.context.get('quiz')
        answers = attrs['answers']
        if not quiz:
            raise ValidationError("El test no existe.")
        if len(answers) != quiz.questions.count():
            raise ValidationError("Faltan respuestas.")
        for answer in answers:
            question_id = answer['question']
            question = QuestionModel.objects.filter(id=question_id).first()
            if not question:
                raise ValidationError("Una de las preguntas no existe.")
            if len(list(question.answers)) <= answer['answer']:
                raise ValidationError(
                    f"No existe la respuesta en la pregunta ({question.question})")
        return super().validate(attrs)

    def create(self, validated_data):
        quiz = self.context.get('quiz')
        user = self.context.get('user')
        user_answers = validated_data['answers']

        formated_answers = list(map(
            lambda answer: answer['answer'], user_answers))
        
        # Create QuizResultModel instance
        result = QuizResultModel.objects.create(
            quiz=quiz,
            user=user,
            answers=formated_answers
        )
        return result


class MakeQuizResponseSerializer(serializers.Serializer):
    quiz = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    correct_answers = serializers.IntegerField(read_only=True)
    score = serializers.FloatField(read_only=True)
    passed = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        return {
            'quiz': instance.quiz.title,
            'correct_answers': instance.correct_answers,
            'score': instance.score,
            'passed': instance.passed,
            'total_questions': instance.quiz.questions.count()
        }
