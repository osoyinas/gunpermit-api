from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from metrics_app.models import TopicMetricsModel
from metrics_app.serializers import ResultsSerializer, TopicMetricsSerializer
from metrics_app.pagination import CustomPagination
from rest_framework.response import Response
from tracking_app.models import UserQuestionAttemptModel
from django.db import models
from questions_app.models import QuestionModel, TopicModel
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserQuestionAttemptsResponseSerializer


class ListUserResults (generics.ListAPIView):
    serializer_class = ResultsSerializer
    queryset = ResultsSerializer.Meta.model.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')


class ListTopicResults (generics.ListAPIView):
    serializer_class = TopicMetricsSerializer
    queryset = TopicMetricsModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TopicMetricsModel.objects.filter(user=self.request.user)


class UserQuestionAttemptsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserQuestionAttemptsResponseSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        attempts = UserQuestionAttemptModel.objects.filter(user=user)
        topics = TopicModel.objects.all()
        topic_data = {}
        for topic in topics:
            topic_attempts = attempts.filter(question__topic=topic)
            print('topic_attempts', topic_attempts)
            correct = topic_attempts.filter(is_correct=True).count()
            incorrect = topic_attempts.filter(is_correct=False).count()
            total = topic.questions.count()
            answered = topic_attempts.count()
            topic_data[topic.title] = {
                "answered": answered,
                "total": total,
                "correct": correct,
                "incorrect": incorrect
            }
        total_answered = attempts.count()
        total_questions = QuestionModel.objects.count()
        total_correct = attempts.filter(is_correct=True).count()
        total_incorrect = attempts.filter(is_correct=False).count()
        data = {
            "topics": topic_data,
            "answered": total_answered,
            "correct": total_correct,
            "incorrect": total_incorrect,
            "total": total_questions
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)