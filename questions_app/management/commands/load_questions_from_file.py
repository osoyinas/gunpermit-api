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

        # Load questions from tema_X.json files
        data_dir = 'data'
        id = 0
        for file_name in os.listdir(data_dir):
            if file_name.startswith('tema_') and file_name.endswith('.json'):
                topic_id = int(file_name.split('_')[1].split('.')[0])
                topic = TopicModel.objects.get(id=topic_id)
                file_path = os.path.join(data_dir, file_name)
                with open(file_path, 'r', encoding='utf-8') as questions_file:
                    questions_data = json.load(questions_file)
                    for question_data in questions_data:
                        answers = question_data['options']
                        correct_answer_index = question_data['answer']
                        formatted_answers = [
                            {'answer': answer, 'is_true': (i == correct_answer_index)}
                            for i, answer in enumerate(answers)
                        ]
                        QuestionModel.objects.create(
                            id=id,
                            question=question_data['question'],
                            answers=formatted_answers,
                            topic=topic
                        )
                        id += 1

        self.stdout.write(self.style.SUCCESS('Successfully loaded topics and questions from JSON files'))