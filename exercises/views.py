from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise , Program
from .serializers import ExerciseSerializer , ProgramSerializer
from accounts.models import Profile


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


@api_view(["POST"])
def make_program(request,coach_id,trainer_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    print(coach.user.username)
    trainer = get_object_or_404(Profile,user__id=trainer_id)
    print(trainer.user.username)
    print("H"*50)
    exercises_ids = request.data.get("exercises",[])

    program = Program.objects.filter(trainer=trainer).first()

    if program:
        return Response({"detail": "This User already got a trainning program"}, status=status.HTTP_400_BAD_REQUEST)
    if not exercises_ids:
        return Response({"detail": "At least one exercise must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    print("H"*50)
    print(exercises_ids[0])
    exercises = Exercise.objects.filter(exercise_id__in=exercises_ids)
    print("K"*50)
    print(exercises[0])
    if exercises.count() != len(exercises_ids):
        return Response(
            {"detail": "One or more exercises not found."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
  
    program = Program.objects.create(
        coach=coach,
        trainer=trainer,
        description = request.data.get("description"),
    )

    program.exercises.set(exercises)
    
    serialized_program = ProgramSerializer(program)
    return Response(serialized_program.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_program(request,user_id):
    trainner = get_object_or_404(Profile,user__id=user_id)
    program =  get_object_or_404(Program,trainer=trainner)
    serialized_program = ProgramSerializer(program)
    return Response(serialized_program.data, status=status.HTTP_201_CREATED)


## NEED ADD 
@api_view(["DELETE"])
def delete_program(request,program_id,user_id):

    deleter = get_object_or_404(Profile,user__id=user_id)
    program = get_object_or_404(Program,id=program_id)

    if(program and (program.coach==deleter or program.trainer==deleter)):
            program.delete()
            return(Response("Program Deleted Succesfuly"))
    else:
           return(Response("no program with that info"))


@api_view(["Post"])
def update_program(request,coach_id,program_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    print(coach.user.username)
    program = get_object_or_404(Program,id=program_id)

    exercises_ids = request.data.get("exercises",[])

    if not exercises_ids:
        return Response({"detail": "At least one exercise must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    if coach!=program.coach:
        print(program.coach.user.id)
        print(coach_id)
        return Response({"detail":"You Cant update on this program"})
    
    print("H"*50)
    print(exercises_ids[0])
    exercises = Exercise.objects.filter(exercise_id__in=exercises_ids)
    print("K"*50)
    print(exercises[0])

    if exercises.count() != len(exercises_ids):
        return Response(
            {"detail": "One or more exercises not found."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    program.exercises.set(exercises)
    serialized_program = ProgramSerializer(program)
    return Response(serialized_program.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_coach_programs(request,coach_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    programs = Program.objects.filter(coach=coach)

    serializer = ProgramSerializer(programs,many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
