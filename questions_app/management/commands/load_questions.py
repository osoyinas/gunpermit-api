import os
import json
from django.core.management.base import BaseCommand
from questions_app.models import QuestionModel, TopicModel

class Command(BaseCommand):
    help = 'Load topics and questions from JSON files into the database'

    def handle(self, *args, **kwargs):
        # Load topics
        topics_file_path = os.path.join('data', 'topics.json')
        with open(topics_file_path, 'r', encoding='utf-8') as topics_file:
            topics_data = json.load(topics_file)
            for topic_data in topics_data:
                TopicModel.objects.get_or_create(
                    id=topic_data['id'],
                    defaults={'name': topic_data['name']}
                )

        # Load questions
        questions_file_path = os.path.join('data', 'questions.json')
        with open(questions_file_path, 'r', encoding='utf-8') as questions_file:
            questions_data = json.load(questions_file)
            for question_data in questions_data:
                topic_id = question_data['topic']
                topic, created = TopicModel.objects.get_or_create(id=topic_id)
                answers = question_data['answers']
                QuestionModel.objects.create(
                    question=question_data['question'],
                    answers=answers,
                    topic=topic
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded topics and questions from JSON files'))