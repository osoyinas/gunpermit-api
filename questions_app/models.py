from collections.abc import Iterable
from django.db import models


class TopicModel(models.Model):
    name = models.CharField(max_length=100)

class SubtopicModel(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(TopicModel, on_delete=models.CASCADE, related_name="subtopics")

class QuestionModel(models.Model):
    question = models.TextField(max_length=300)
    answers = models.JSONField(default=list)
    topic = models.ForeignKey(TopicModel, on_delete=models.CASCADE, related_name="questions")
    subtopic = models.ForeignKey(SubtopicModel, on_delete=models.CASCADE, related_name="questions")
