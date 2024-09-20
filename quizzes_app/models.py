from django.db import models

from questions_app.models import QuestionModel


class QuizModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField(
        QuestionModel,
        through='QuizQuestionModel',
        related_name='quizzes',
        related_query_name='quiz'
    )

    def __str__(self):
        return self.title


class QuizQuestionModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'question'], name='unique_quiz_question')
        ]