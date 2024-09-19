from questions_app.mocks import createTopicWithQuestionsMock
from quizzes_app.models import QuizModel, QuizQuestionModel


def createQuizMock(title: str = 'Quiz 1'):
    topic = createTopicWithQuestionsMock()
    questions = topic.questions.all()
    quiz = QuizModel.objects.create(title=title)

    quiz_questions = []

    for i, question in enumerate(questions):
        quiz_question = QuizQuestionModel.objects.create(
            quiz=quiz, question=question, order=i)
        quiz_questions.append(quiz_question)
    return quiz
