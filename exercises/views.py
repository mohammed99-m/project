from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise
from .serializers import ExerciseSerializer


@api_view(["GET"])
def list_exercises(request):
    exercises = Exercise.objects.all()  
    serializer = ExerciseSerializer(exercises, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def search_exercises(request):
    query = request.query_params.get('q', None)  
    if query:
        exercises = Exercise.objects.filter(name__icontains=query)  
    else:
        exercises = Exercise.objects.all()  

    serializer = ExerciseSerializer(exercises, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)