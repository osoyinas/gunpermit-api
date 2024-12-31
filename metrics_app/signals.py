from django.db.models.signals import post_save
from django.dispatch import receiver
from auth_app.models import CustomUser
from questions_app.models import QuestionModel, TopicModel
from tracking_app.models import UserQuestionAttemptModel
