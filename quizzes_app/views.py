from rest_framework import generics, permissions, status
from rest_framework.response import Response
from auth_app.permissions import IsAdminOrReadOnly
from metrics_app.pagination import CustomPagination
from quizzes_app.models import QuizCategoryModel, QuizModel
from quizzes_app.serializers import MakeQuizResponseSerializer, MakeQuizSerializer, CreateQuizSerializer, CreateQuizSerializer, QuizCategoryWithQuizAttemptSerializer, QuizSerializer
from drf_yasg.utils import swagger_auto_schema
from auth_app.generics import *


class RetrieveDestroyUpdateQuizAPIView(ReadableRetrieveUpdateDestroyAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = QuizSerializer


class ListCreateQuizApiView(ReadableListCreateAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = CreateQuizSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        category_tag = self.request.query_params.get('category', None)
        if category_tag is not None:
            queryset = queryset.filter(category__tag=category_tag)
        return queryset

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
        serializer = MakeQuizSerializer(data=request.data, context={
                                        'quiz': quiz, 'user': user})

        if serializer.is_valid():
            result = serializer.save()
            response_serializer = MakeQuizResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListQuizCategoriesView(ReadableListAPIView):
    queryset = QuizCategoryModel.objects.all()
    serializer_class = QuizCategoryWithQuizAttemptSerializer
