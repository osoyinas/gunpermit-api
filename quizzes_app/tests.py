from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.mocks import createUserMock, getAuthenticatedClient
from .mocks import createQuizMock


class QuizTests(TestCase):
    def setUp(self):
        self.user = createUserMock()
        self.client = getAuthenticatedClient(self.user)
        self.quiz = createQuizMock()

    def test_retrieve_quiz(self):
        url = reverse('retrieve-destroy-quiz', kwargs={'pk': self.quiz.id})

        response = self.client.get(url)

        print(response.data['questions'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.quiz.title)
        self.assertEqual(response.data['description'], self.quiz.description)
        self.assertIsInstance(response.data['questions'], list)
