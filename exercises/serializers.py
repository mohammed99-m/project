from rest_framework import serializers
from .models import Exercise

class ExerciseSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField(read_only=True) 
    name = serializers.CharField(max_length=255, required=True) 
    muscle_group = serializers.CharField(max_length=255, required=True)  
    #video_url = serializers.URLField(required=False, allow_blank=True) 
    description = serializers.CharField(required=False, allow_blank=True) 

  