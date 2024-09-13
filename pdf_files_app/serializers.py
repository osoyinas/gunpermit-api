from rest_framework import serializers
from .models import PDFFile
from questions_app.serializers import TopicSerializer
from questions_app.models import TopicModel, QuestionModel
from .pdf_scrapper import get_text_from, extract_questions_and_answers

class PDFFileSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    class Meta:
        model = PDFFile
        fields = ['id', 'file','name', 'topic', 'created_at']

    def create(self, validated_data):
            pdf_file = PDFFile.objects.create(**validated_data)
            pdf_file.name = pdf_file.file.name.split('/')[-1]
            pdf_content = get_text_from(pdf_file.file.path)
            pdf_data = extract_questions_and_answers(pdf_content)
            topic_model = TopicModel.objects.create(name=pdf_data["topic"])
            topic_model.save()
            for question in pdf_data['questions']:
                question_model = QuestionModel.objects.create(topic=topic_model, question=question['question'], answers=question['answers'])
                question_model.save()
            pdf_file.topic = topic_model
            pdf_file.save()
            return pdf_file