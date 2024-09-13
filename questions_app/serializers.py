from rest_framework import serializers
from .models import TopicModel, QuestionModel 
from django.contrib.auth import get_user_model

User = get_user_model()

ANSWERS_STRUCTURE = [{'answer': str, 'is_true': bool}] * 3
DEFAULT_ANSWERS = [{'answer': "respuesta", 'is_true': False}] * 3

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField()
    class Meta:
        model = QuestionModel
        fields = ['id','topic', 'question', 'answers']
    
    def validate_answers(self, answers):
        """
        Validación personalizada para el campo 'answers' para que coincida con la estructura de ANSWERS_STRUCTURE
        """
        if not isinstance(answers, list):
            raise serializers.ValidationError("El campo 'answers' debe ser una lista.")
        if len(answers) != len(ANSWERS_STRUCTURE):
            raise serializers.ValidationError(f"El campo 'answers' debe tener exactamente {len(ANSWERS_STRUCTURE)} elementos.")
        
        for expected_answer, received_answer in zip(ANSWERS_STRUCTURE, answers):
            if not isinstance(received_answer, dict):
                raise serializers.ValidationError("Cada elemento en 'answers' debe ser un diccionario.")
            
            for key, expected_type in expected_answer.items():
                if key not in received_answer:
                    raise serializers.ValidationError(f"Falta la clave '{key}' en uno de los elementos de 'answers'.")
                
                if not isinstance(received_answer[key], expected_type):
                    raise serializers.ValidationError(f"El valor de '{key}' en 'answers' debe ser de tipo {expected_type}.")

        return answers


class TopicSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = TopicModel
        fields = ['id', 'name', 'questions']
    
    




