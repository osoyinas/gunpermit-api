from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from questions_app.serializers import QuestionSerializer, TopicCreationSerializer
from .models import TopicModel, QuestionModel
from unittest import skip

class TopicTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        topicA_data = {'name': 'Topic 1', 'subtopics': [{'name': 'Subtopic 1'}, {'name': 'Subtopic 2'}]}
        topicA = TopicCreationSerializer(data = topicA_data)
        topicA.is_valid(raise_exception=True)
        self.topicA = topicA.save()

        topicB_data = {'name': 'Topic 2', 'subtopics': [{'name': 'Subtopic 3'}, {'name': 'Subtopic 4'}]}
        topicB = TopicCreationSerializer(data = topicB_data)
        topicB.is_valid(raise_exception=True)
        self.topicB = topicB.save()


    def test_list_create_topics_view(self):
        response = self.client.get(reverse('list_create_topics'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_topics_view(self):
        response = self.client.get(reverse('retrieve_topics', kwargs={'pk': self.topicA.id}))    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Topic 1')


class QuestionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        data = {'name': 'Topic 1', 'subtopics': [{'name': 'Subtopic 1'}, {'name': 'Subtopic 2'}]}

        topic_serializer = TopicCreationSerializer(data = data)
        topic_serializer.is_valid(raise_exception=True)
        self.topic = topic_serializer.save()
        self.question = QuestionModel.objects.create(question='Question1',answers=[{'answer': 'Respuesta 1', 'is_true': True}, {'answer': 'Respuesta 2', 'is_true': False}, {'answer': 'Respuesta 3', 'is_true': False}],  topic=self.topic, subtopic=self.topic.subtopics.first())


    def test_create_question_view(self):
        url = reverse('list_create_questions')
        data = {'topic': self.topic.id, 'subtopic': self.topic.subtopics.first().id, 'question': 'Pregunta 1', 'answers': [{'answer': 'Respuesta 1', 'is_true': True}, {'answer': 'Respuesta 2', 'is_true': False}, {'answer': 'Respuesta 3', 'is_true': False}]}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_list_questions_topic_view(self):
        url = reverse('list_questions_topic', kwargs={'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)