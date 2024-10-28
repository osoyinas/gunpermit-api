from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from metrics_app.models import TopicMetricsModel
from metrics_app.serializers import ResultsSerializer, TopicMetricsSerializer
from metrics_app.pagination import CustomPagination


class ListUserResults (generics.ListAPIView):
    serializer_class = ResultsSerializer
    queryset = ResultsSerializer.Meta.model.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')


class ListTopicResults (generics.ListAPIView):
    serializer_class = TopicMetricsSerializer
    queryset = TopicMetricsModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TopicMetricsModel.objects.filter(user=self.request.user)
