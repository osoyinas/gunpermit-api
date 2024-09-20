from rest_framework import generics, permissions

from auth_app.permissions import IsAdminOrReadOnly
from quizzes_app.models import QuizModel
from quizzes_app.serializers import QuizSerializer


class RetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly,]