from rest_framework import serializers
from .models import IllnessToAvoidFood,IllnessToAvoidExercises

class IllnessToAvoidFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = IllnessToAvoidFood
        fields = ['id','illness','foods_to_avoid','sources']

class IllnessToAvoidExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IllnessToAvoidExercises
        fields = ['id','illness','safer_alternatives','exercise_to_avoid','sources']