from rest_framework import generics, permissions, status
from rest_framework.response import Response
from auth_app.permissions import IsAdminOrReadOnly
from quizzes_app.models import QuizModel
from quizzes_app.serializers import MakeQuizResponseSerializer, MakeQuizSerializer, QuizCreateSerializer, QuizSerializer
from drf_yasg.utils import swagger_auto_schema


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
    

class MakeQuizAPIView(generics.GenericAPIView):
    queryset = QuizModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        quiz_id = self.kwargs.get('pk')
        return generics.get_object_or_404(QuizModel, pk=quiz_id)

    @swagger_auto_schema(
        request_body=MakeQuizSerializer,
        responses={201: MakeQuizResponseSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        user = request.user
        serializer = MakeQuizSerializer(data=request.data, context={'quiz': quiz, 'user': user})
        
        if serializer.is_valid():
            result = serializer.save()
            response_serializer = MakeQuizResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
