from rest_framework import generics
from auth_app.permissions import IsAdminOrReadOnly
from metrics_app.pagination import CustomPagination
from metrics_app.serializers import ResultsSerializer


class ListUserResults (generics.ListAPIView):
    serializer_class = ResultsSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ResultsSerializer.Meta.model.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')
