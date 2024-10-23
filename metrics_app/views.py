from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from questions_app.models import TopicModel, QuestionModel
from questions_app.models import UserQuestionAttemptModel
from metrics_app.serializers import ResultsSerializer, TopicResultsListSerializer
from metrics_app.pagination import CustomPagination


class ListUserResults (generics.ListAPIView):
    serializer_class = ResultsSerializer
    queryset = ResultsSerializer.Meta.model.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')


class ListTopicResults (generics.ListAPIView):
    serializer_class = TopicResultsListSerializer
    queryset = UserQuestionAttemptModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Get topic results for the authenticated user",
        responses={200: openapi.Response(
            'A list of topic results', TopicResultsListSerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        question_attempts = self.get_queryset()
        topics = TopicModel.objects.all()
        results = []

        for topic in topics:
            total_questions_for_topic = QuestionModel.objects.filter(
                topic=topic).count()
            topic_attempts = question_attempts.filter(question__topic=topic)
            correct_attempts = 0

            for attempt in topic_attempts:
                if (attempt.is_correct):
                    correct_attempts += 1
            results.append(
                {
                    'topic': str(topic.name),
                    'mark': correct_attempts,
                    'full_mark': total_questions_for_topic
                }
            )
        
        serializer = TopicResultsListSerializer(data=results)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
