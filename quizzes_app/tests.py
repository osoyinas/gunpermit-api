from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.mocks import createUserMock, createUserStaffMock, getAuthenticatedClient
from .mocks import createQuizMock


class QuizTests(TestCase):
    def setUp(self):
        self.user = createUserMock()
        self.staff_user = createUserStaffMock(email='staff@gmail.com', username='staff')
        self.client = getAuthenticatedClient(self.user)
        self.staff_client = getAuthenticatedClient(self.staff_user)
        self.quiz = createQuizMock()

    def test_retrieve_quiz(self):
        url = reverse('retrieve-destroy-quiz', kwargs={'pk': self.quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.quiz.title)
        self.assertEqual(response.data['description'], self.quiz.description)
        self.assertIsInstance(response.data['questions'], list)


    def test_create_quiz(self):
        url = reverse('create-quiz')
        data = {
            'title': 'Test Quiz',
            'description': 'Test Description',
            'questions': [1, 2, 3]
        }
        
        response = self.staff_client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertIsInstance(response.data['questions'], list)
        self.assertEqual(len(response.data['questions']), 3)