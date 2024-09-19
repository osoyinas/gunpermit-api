from questions_app.models import QuestionModel, TopicModel


def createQuestionMock(topic: TopicModel, question: str = 'Question 1'):
    return QuestionModel.objects.create(
        question=question,
        answers=[{'answer': 'Respuesta 1', 'is_true': True},
                 {'answer': 'Respuesta 2', 'is_true': False},
                 {'answer': 'Respuesta 3', 'is_true': False}
                 ],
        topic=topic)


def createTopicMock(name: str = 'Topic 1'):
    return TopicModel.objects.create(name=name)


def createTopicWithQuestionsMock():
    topic = createTopicMock()
    createQuestionMock(topic)
    createQuestionMock(topic, 'Question 2')
    createQuestionMock(topic, 'Question 3')
    return topic
