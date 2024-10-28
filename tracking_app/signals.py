from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuizResultModel, UserQuestionAttemptModel


@receiver(post_save, sender=QuizResultModel)
def quiz_result_created(sender, instance: QuizResultModel, created, **kwargs):
    return
