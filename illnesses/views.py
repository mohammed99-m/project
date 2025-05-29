from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import IllnessToAvoidFood,IllnessToAvoidExercises
from rest_framework.response import Response
from rest_framework import status
from .serializers import IllnessToAvoidFoodSerializer,IllnessToAvoidExercisesSerializer
# Create your views here.

@api_view(['DELETE'])
def delete_all_illnesses(request):
    count = IllnessToAvoidFood.objects.count()
    IllnessToAvoidFood.objects.all().delete()
    return Response(
        {'message': f'All {count} illness records deleted successfully.'},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def add_illnisses_list(request):
    illnesses_data = request.data
    created_illnesses = []

    for illness in illnesses_data:
        try:
            obj, created = IllnessToAvoidFood.objects.update_or_create(
                illness=illness.get('illness'),
                defaults={
                    'illness': illness.get('illness'),
                    'foods_to_avoid': illness.get('foods_to_avoid'),
                    'sources':illness.get('sources')
                }
            )
            created_illnesses.append({
                'illnesses_id': obj.id,
                'created': created
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'illnesses added successfully.', 'results': created_illnesses}, status=status.HTTP_201_CREATED)
  

@api_view(['GET'])
def list_illnesses(request):
    illnesses = IllnessToAvoidFood.objects.all()
    serializer = IllnessToAvoidFoodSerializer(illnesses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_illnisses_exercises_list(request):
    illnesses_data = request.data
    created_illnesses = []

    for illness in illnesses_data:
        try:
            obj, created = IllnessToAvoidExercises.objects.update_or_create(
                illness = illness.get('illness'),
                defaults={
                    'illness': illness.get('illness'),
                    'exercise_to_avoid': illness.get('exercises_to_avoid'),
                    'safer_alternatives':illness.get('safer_alternatives'),
                    'sources':illness.get('sources')
                }
            )
            created_illnesses.append({
                'illnesses_id': obj.id,
                'created': created
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'illnesses added successfully.', 'results': created_illnesses}, status=status.HTTP_201_CREATED)
  
@api_view(['GET'])
def list_illnesses_exercises(request):
    illnesses = IllnessToAvoidExercises.objects.all()
    serializer = IllnessToAvoidExercisesSerializer(illnesses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
