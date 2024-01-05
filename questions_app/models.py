from django.db import models


class TopicModel(models.Model):
    name = models.CharField(max_length=100)


class QuestionModel(models.Model):
    question = models.TextField(max_length=300)
    answers = models.JSONField(default=list)
    topic = models.ForeignKey(TopicModel, on_delete=models.CASCADE, related_name="questions")
