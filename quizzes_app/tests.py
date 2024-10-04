from django.test import TestCase
from django.urls import reverse
from auth_app.mocks import createUserMock, createUserStaffMock, getAuthenticatedClient
from questions_app.models import QuestionModel, TopicModel
from quizzes_app.models import QuizModel, QuizQuestionModel
from quizzes_app.serializers import MakeQuizSerializer
from .mocks import createQuizMock


class QuizTests(TestCase):
    def setUp(self):
        self.user = createUserMock()
        self.staff_user = createUserStaffMock(
            email='staff@gmail.com', username='staff')
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


class MakeQuizSerializerTest(TestCase):
    def setUp(self):
        self.user = createUserMock()
        self.quiz = createQuizMock()
        self.questions = list(self.quiz.questions.all())

    def test_make_quiz_serializer_valid(self):
        data = {
            'answers': [
                {'question': self.questions[0].id, 'answer': 0},
                {'question': self.questions[1].id, 'answer': 1},
                {'question': self.questions[2].id, 'answer': 0},
            ]
        }
        context = {'quiz': self.quiz, 'user': self.user}
        serializer = MakeQuizSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid())
        serializer.save()


class MakeQuizAPITestCase(TestCase):
    def setUp(self):
        self.user = createUserMock()
        self.client = getAuthenticatedClient(self.user)

        self.topic = TopicModel.objects.create(name='Sample Topic')
        self.quiz = QuizModel.objects.create(title='Sample Quiz')

        self.questions = [
            QuestionModel.objects.create(topic=self.topic, question='Question 1', answers=[
                {'answer': 'Answer1', 'is_true': False},
                {'answer': 'Answer 2', 'is_true': True},
                {'answer': 'Answer 3', 'is_true': False},
            ]),
            QuestionModel.objects.create(topic=self.topic, question='Question 2', answers=[
                {'answer': 'Answer1', 'is_true': False},
                {'answer': 'Answer 2', 'is_true': True},
                {'answer': 'Answer 3', 'is_true': False},
        ]),
            QuestionModel.objects.create(topic=self.topic, question='Question 3', answers=[
                {'answer': 'Answer1', 'is_true': False},
                {'answer': 'Answer 2', 'is_true': True},
                {'answer': 'Answer 3', 'is_true': False},
            ]),
        ]

        for question in self.questions:
            QuizQuestionModel.objects.create(quiz=self.quiz, question=question)

    def test_make_quiz(self):
        url = reverse('make-quiz', kwargs={'pk': self.quiz.pk})
        data = {
            'answers': [
                {'question': self.questions[0].id, 'answer': 0},
                {'question': self.questions[1].id, 'answer': 1},
                {'question': self.questions[2].id, 'answer': 0},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('quiz', response.data)
        self.assertIn('user', response.data)
        self.assertIn('correct_answers', response.data)
        self.assertIn('score', response.data)
        self.assertIn('passed', response.data)
