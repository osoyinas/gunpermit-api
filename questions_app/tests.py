from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from auth_app.mocks import createUserStaffMock, getAuthenticatedClient
from .models import TopicModel, QuestionModel


class TopicTests(TestCase):
    def setUp(self):
        self.staff_user = createUserStaffMock(
            email='staff@gmail.com', username='staff')
        self.client = getAuthenticatedClient(self.staff_user)
        self.topicA = TopicModel.objects.create(name='Topic 1')
        self.topicB = TopicModel.objects.create(name='Topic 2')

    def test_list_create_topics_view(self):
        response = self.client.get(reverse('list_create_topics'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_topics_view(self):
        response = self.client.get(
            reverse('retrieve_topics', kwargs={'pk': self.topicA.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Topic 1')


class QuestionTests(TestCase):
    def setUp(self):
        self.staff_user = createUserStaffMock(
            email='staff@gmail.com', username='staff')
        self.client = getAuthenticatedClient(self.staff_user)
        self.topic = TopicModel.objects.create(name='Topic 1')
        self.question = QuestionModel.objects.create(question='Question 1',
                                                     answers=[
                                                         {'answer': 'Respuesta 1',
                                                             'is_true': True},
                                                         {'answer': 'Respuesta 2',
                                                             'is_true': False},
                                                         {'answer': 'Respuesta 3',
                                                          'is_true': False}],
                                                     topic=self.topic)

    def test_create_question_view(self):
        url = reverse('list_create_questions')
        data = {'topic': self.topic.id,
                'question': 'Pregunta 1',
                'answers': [
                    {'answer': 'Respuesta 1', 'is_true': True},
                    {'answer': 'Respuesta 2', 'is_true': False},
                    {'answer': 'Respuesta 3', 'is_true': False}
                ]}

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_questions_topic_view(self):
        url = reverse('list_questions_topic', kwargs={
                      'topic_id': self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_question_view(self):
        url = reverse('retrieve_destroy_update_question',
                      kwargs={'pk': self.question.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_question_view(self):
        url = reverse('retrieve_destroy_update_question',
                      kwargs={'pk': self.question.id})
        data = {'question': 'Pregunta 2',
                'answers': [
                    {'answer': 'Respuesta 1', 'is_true': True},
                    {'answer': 'Respuesta 2', 'is_true': False},
                    {'answer': 'Respuesta 3', 'is_true': False}
                ]}

        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
