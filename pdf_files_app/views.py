from rest_framework import generics, parsers
from .serializers import PDFFileSerializer
from .models import PDFFile

class CreateListPDFView(generics.ListCreateAPIView):
    serializer_class = PDFFileSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    queryset = PDFFile.objects.all()

    def perform_create(self, serializer):
        serializer.save(file=self.request.data.get('file'))

class DeletePDFView(generics.DestroyAPIView):
    serializer_class = PDFFileSerializer
    queryset = PDFFile.objects.all()

class DeleteAllPDFView(generics.DestroyAPIView):
    serializer_class = PDFFileSerializer
    queryset = PDFFile.objects.all()

    def delete(self, request, *args, **kwargs):
        PDFFile.objects.all().delete()
        return self.destroy(request, *args, **kwargs)
# class CreateTopicFromPDFView(generics.GenericAPIView):
#     serializer_class = PDFFileSerializer
#     queryset = PDFFile.objects.all()

#     def post(self, request, *args, **kwargs):
#         file = PDFFile.objects.get(pk=self.kwargs['pk'])
#         topic = file.topic
#         topic.save()
#         return self.destroy(request, *args, **kwargs)