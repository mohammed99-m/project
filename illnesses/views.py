from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

from accounts.models import Profile
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

@api_view(['GET'])
def get_exercises_to_avoid_for_user(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)

    illness = profile.illnesses
    if not illness:
        return Response({'error': 'No illness recorded for this user.'}, status=status.HTTP_404_NOT_FOUND)
    print(illness)
    illness_data = IllnessToAvoidExercises.objects.filter(illness__in=illness)
    print(illness_data)
    
    if not illness_data:
        return Response({'message': 'No data available for this illness.'}, status=status.HTTP_204_NO_CONTENT)

    exercise_to_avoid = []
    safer_alternatives = []
    sources = []

    for illnes in illness_data:
        exercise_to_avoid.extend(illnes.exercise_to_avoid)
        safer_alternatives.extend(illnes.safer_alternatives)
        sources.extend(illnes.sources)

    exercise_to_avoid = list(set(exercise_to_avoid))
    safer_alternatives = list(set(safer_alternatives))
    sources = list(set(sources))

    return Response({
        'illnesses': illness,
        'exercises_to_avoid': exercise_to_avoid,
        'safer_alternatives': safer_alternatives,
        'sources': sources,
    }, status=status.HTTP_200_OK)

    # return Response({
    #     'illness': illness,
    #     'exercises_to_avoid': illness_data.exercise_to_avoid,
    #     'safer_alternatives': illness_data.safer_alternatives,
    #     'sources': illness_data.sources
    # }, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_foods_to_avoid_for_user(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)

    illnesses = profile.illnesses
    if not illnesses:
        return Response({'error': 'No illnesses recorded for this user.'}, status=status.HTTP_404_NOT_FOUND)

    illness = IllnessToAvoidFood.objects.filter(illness__in=illnesses)

    if not illness.exists():
        return Response({'message': 'No data available for these illnesses.'}, status=status.HTTP_204_NO_CONTENT)

    food_to_avoid = []
    sources = []

    for illnes in illness:
        food_to_avoid.extend(illnes.foods_to_avoid)
        sources.extend(illnes.sources)

    food_to_avoid = list(set(food_to_avoid))
    sources = list(set(sources))

    return Response({
        'illnesses': illnesses,
        'foods_to_avoid': food_to_avoid,
        'sources': sources,
    }, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def force_delete_illnesses_food(request,illnesses_id):
    try:
         illnesses = get_object_or_404(IllnessToAvoidFood,id=illnesses_id)
         illnesses.delete()
         return Response({"message":"Illnesses deleted successfully."},status=status.HTTP_200_OK)
    except IllnessToAvoidFood.DoesNotExist:
        return Response({"message":"Something get Wrong"},status=status.HTTP_200_OK)
    
@api_view(["DELETE"])
def force_delete_illnesses_exercises(request,illnesses_id):
    try:
         illnesses = get_object_or_404(IllnessToAvoidExercises,id=illnesses_id)
         illnesses.delete()
         return Response({"message":"Illnesses deleted successfully."},status=status.HTTP_200_OK)
    except IllnessToAvoidExercises.DoesNotExist:
        return Response({"message":"Something get Wrong"},status=status.HTTP_200_OK)
