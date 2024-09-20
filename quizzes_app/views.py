from rest_framework import generics, permissions, status
from rest_framework.response import Response
from auth_app.permissions import IsAdminOrReadOnly
from quizzes_app.models import QuizModel
from quizzes_app.serializers import QuizCreateSerializer, QuizSerializer


class RetrieveDestroyQuizAPIView(generics.RetrieveDestroyAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAdminOrReadOnly,]


class CreateQuizAPIView(generics.CreateAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = serializer.save()
        
        # Use the QuizSerializer to return the quiz with its questions
        read_serializer = QuizSerializer(quiz)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)