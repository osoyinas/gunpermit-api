import os
from django.conf import settings
from django.db import models
from questions_app.models import TopicModel

class PDFFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')
    topic = models.OneToOneField(TopicModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, self.file.path)
        if os.path.isfile(file_path):
            os.remove(file_path)
        if self.topic:
            self.topic.delete()
        super(PDFFile, self).delete(*args, **kwargs)