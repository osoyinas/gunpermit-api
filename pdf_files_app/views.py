from rest_framework import generics, parsers
from .serializers import PDFFileSerializer
from .models import PDFFile
from rest_framework import permissions

class CreateListPDFView(generics.ListCreateAPIView):
    serializer_class = PDFFileSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    queryset = PDFFile.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(file=self.request.data.get('file'))

class DeletePDFView(generics.DestroyAPIView):
    serializer_class = PDFFileSerializer
    queryset = PDFFile.objects.all()
    permission_classes = [permissions.IsAdminUser]

class DeleteAllPDFView(generics.DestroyAPIView):
    serializer_class = PDFFileSerializer
    queryset = PDFFile.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        PDFFile.objects.all().delete()
        return self.destroy(request, *args, **kwargs)
