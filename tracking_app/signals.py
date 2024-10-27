from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuizResultModel


@receiver(post_save, sender=QuizResultModel)
def quiz_result_created(sender, instance, created, **kwargs):
    if created:
        # Aquí puedes agregar la lógica que deseas ejecutar cuando se crea un QuizResultModel
        print(f'QuizResultModel creado: {instance}')
