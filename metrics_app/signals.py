from django.db.models.signals import post_save
from django.dispatch import receiver
from auth_app.models import CustomUser
from questions_app.models import QuestionModel, TopicModel
from tracking_app.models import UserQuestionAttemptModel
from .models import TopicMetricsModel


# Create the topic metrics for the new user
@receiver(post_save, sender=CustomUser)
def user_created(sender, instance: CustomUser, created, **kwargs):
    if (created):
        for topic in TopicModel.objects.all():
            TopicMetricsModel.objects.create(
                user=instance,
                topic=topic,
                mark=0
            )


@receiver(post_save, sender=UserQuestionAttemptModel)
def quiz_result_created(sender, instance: UserQuestionAttemptModel, created, **kwargs):
    user = instance.user
    topic = instance.question_with_answer.question.topic

    # Get the topic metrics
    try:
        topic_metric = TopicMetricsModel.objects.get(
            user=user,
            topic=topic
        )
    except TopicMetricsModel.DoesNotExist:
        topic_metric = TopicMetricsModel.objects.create(
            user=user,
            topic=topic,
            mark=0
        )

    # Update the mark of the topic metric
    if (created):
        if (instance.is_correct):
            topic_metric.mark += 1
        else:
            topic_metric.mark -= 1
    else:
        if (not instance.is_correct):
            topic_metric.mark -= 1

    topic_metric.save()
