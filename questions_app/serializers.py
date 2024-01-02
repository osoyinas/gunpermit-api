from rest_framework import serializers
from .models import TopicModel, SubtopicModel, QuestionModel 

ANSWERS_STRUCTURE = [{'answer': str, 'is_true': bool}] * 3
DEFAULT_ANSWERS = [{'answer': "respuesta", 'is_true': False}] * 3


class SubtopicSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    class Meta:
        model = SubtopicModel
        fields = ['id', 'name', 'questions', 'topic']
    
    def get_questions(self, obj):
        return obj.questions.count()

class SubtopicCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtopicModel
        fields = ['id', 'name']

class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True)
    questions = serializers.SerializerMethodField()
    
    class Meta:
        model = TopicModel
        fields = ['id', 'name', 'subtopics', 'questions']

    def get_questions(self, obj):
        return obj.questions.count() 
    
class TopicCreationSerializer(serializers.ModelSerializer):
    subtopics = SubtopicCreationSerializer(many=True)

    class Meta:
        model = TopicModel
        fields = ['id', 'name', 'subtopics']

    def create(self, validated_data):
        subtopics_data = validated_data.pop('subtopics', [])
        topic = TopicModel.objects.create(**validated_data)
        for subtopic in subtopics_data:
            subtopic['topic'] = topic.id
            subtopic_serializer = SubtopicSerializer(data=subtopic)
            subtopic_serializer.is_valid(raise_exception=True)
            subtopic_serializer.save()
        return topic
    

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField()
    class Meta:
        model = QuestionModel
        fields = ['id', 'topic', 'subtopic', 'question', 'answers']
    
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


