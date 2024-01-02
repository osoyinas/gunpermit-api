from rest_framework import generics, permissions
from .models import TopicModel, SubtopicModel, QuestionModel
from .serializers import TopicSerializer, TopicCreationSerializer, SubtopicSerializer, QuestionSerializer


class ListCreateTopicsView(generics.ListCreateAPIView):
    queryset = TopicModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TopicCreationSerializer
        return TopicSerializer



class RetrieveTopicsView(generics.RetrieveAPIView):
    queryset = TopicModel.objects.all()
    serializer_class = TopicSerializer



class ListCreateQuestionsView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = QuestionModel.objects.all()


class ListQuestionsTopicView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self, *args, **kwargs):
        # Obtiene el <topic_id> de la URL
        topic_id = self.kwargs.get('topic_id')    
        queryset = QuestionModel.objects.filter(topic__id=topic_id)
        return queryset
