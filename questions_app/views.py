from rest_framework import generics, permissions

from auth_app.permissions import IsAdminOrReadOnly
from .models import TopicModel, QuestionModel
from .serializers import TopicSerializerWithQuestions, QuestionSerializer


class ListCreateTopicsView(generics.ListCreateAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializerWithQuestions
    permission_classes = [IsAdminOrReadOnly, ]


class RetrieveUpdateDestroyTopicsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializerWithQuestions
    permission_classes = [IsAdminOrReadOnly]


class ListCreateQuestionsView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = QuestionModel.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]


class ListQuestionsTopicView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # Obtiene el <topic_id> de la URL
        topic_id = self.kwargs.get('topic_id')
        queryset = QuestionModel.objects.filter(topic__id=topic_id)
        return queryset


class RetrieveDestroyUpdateQuestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly, ]
