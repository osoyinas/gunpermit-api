from django.db import models
from auth_app.models import CustomUser
from questions_app.models import TopicModel


class TopicMetricsModel(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='metrics')
    topic = models.ForeignKey(
        TopicModel, on_delete=models.CASCADE, related_name="metrics")
    mark = models.IntegerField()

    class Meta:
        unique_together = ('user', 'topic')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'topic'], name='unique_user_topic_metric')
        ]

    @property
    def full_mark(self):
        return self.topic.questions.count()

    def __str__(self):
        return f'{self.topic} - {self.mark}/{self.full_mark}'
