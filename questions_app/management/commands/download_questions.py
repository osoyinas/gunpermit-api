import json
from django.core.management.base import BaseCommand
from questions_app.models import QuestionModel, TopicModel
from questions_app.serializers import QuestionSerializer, TopicSerializer


class Command(BaseCommand):
    help = 'Export QuestionModel and TopicModel to JSON'

    def handle(self, *args, **kwargs):
        # Export Topics
        topics = TopicModel.objects.all()
        topics_data = TopicSerializer(topics, many=True).data
        with open('topics.json', 'w', encoding='utf-8') as topics_file:
            json.dump(topics_data, topics_file, ensure_ascii=False, indent=4)

        # Export Questions
        questions = QuestionModel.objects.all()
        questions_data = QuestionSerializer(questions, many=True).data
        with open('questions.json', 'w', encoding='utf-8') as questions_file:
            json.dump(questions_data, questions_file,
                      ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(
            'Successfully exported models to JSON'))
