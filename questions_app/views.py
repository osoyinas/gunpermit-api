from rest_framework import generics, permissions

from auth_app.permissions import IsAdminOrReadOnly
from auth_app.generics import *
from .models import TopicModel, QuestionModel
from .serializers import TopicSerializer, QuestionSerializer
from oauth2_provider.contrib.rest_framework.permissions import (
    IsAuthenticatedOrTokenHasScope,
)


class ListTopicsView(ReadableListAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializer


class RetrieveUpdateDestroyTopicsView(ReadableRetrieveUpdateDestroyAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializer


class ListQuestionsView(ReadableListAPIView):
    serializer_class = QuestionSerializer
    queryset = QuestionModel.objects.all()
    permission_classes = [
        IsAuthenticatedOrTokenHasScope,
    ]
    required_scopes = ["read"]


class ListQuestionsTopicView(ReadableListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ["read"]

    def get_queryset(self, *args, **kwargs):
        # Obtiene el <topic_id> de la URL
        topic_id = self.kwargs.get("topic_id")
        queryset = QuestionModel.objects.filter(topic__id=topic_id)
        return queryset


class RetrieveDestroyUpdateQuestionView(ReadableRetrieveUpdateDestroyAPIView):
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrTokenHasScope]
