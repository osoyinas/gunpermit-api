from rest_framework import generics, permissions

from quizzes_app.models import QuizModel
from quizzes_app.serializers import QuizSerializer


class RetrieveQuiz(generics.RetrieveAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = QuizSerializer
