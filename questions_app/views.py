from rest_framework import generics, permissions
from .models import TopicModel, QuestionModel
from .serializers import TopicSerializer, QuestionSerializer


class ListCreateTopicsView(generics.ListCreateAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser,]
        else:
            self.permission_classes = [permissions.IsAuthenticated,]
        return super().get_permissions()


class RetrieveUpdateDestroyTopicsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser,]
        else:
            self.permission_classes = [permissions.IsAuthenticated,]
        return super().get_permissions()


class ListCreateQuestionsView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = QuestionModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser,]
        else:
            self.permission_classes = [permissions.IsAuthenticated,]
        return super().get_permissions()


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

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser,]
        else:
            self.permission_classes = [permissions.IsAuthenticated,]
        return super().get_permissions()
