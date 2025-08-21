import os
import random
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from illnesses.models import IllnessToAvoidExercises
from .models import Exercise, ExerciseSchedule , Program
from .serializers import ExerciseSerializer , ProgramSerializer
from .models import Profile
import joblib
import numpy as np


#للحصول على التمارين

@api_view(["GET"])
def list_exercises(request):
    exercises = Exercise.objects.all()  
    serializer = ExerciseSerializer(exercises, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

#للبحث عن تمرين حسب الاسم
@api_view(["GET"])
def search_exercises(request):
    query = request.query_params.get('q', None)  
    if query:
        exercises = Exercise.objects.filter(name__icontains=query)  # icontains فلترة تمارين تحتوي على النص بدون تمييز بين الأحرف
    else:
        exercises = Exercise.objects.all()  

    serializer = ExerciseSerializer(exercises, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

#لصناعة برنامج رياضي لمتدرب محدد
@api_view(["POST"])
def make_program(request,coach_id,trainer_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    print(coach.user.username)
    trainer = get_object_or_404(Profile,user__id=trainer_id)
    print(trainer.user.username)
    print("H"*50)
# استقبل البيانات المتعلقة بالأيام والتمارين
    days_exercises = request.data.get("days_exercises", [])
    print(days_exercises)
    program = Program.objects.filter(trainer=trainer).first()

    if program:
        return Response({"detail": "This User already got a trainning program"}, status=status.HTTP_400_BAD_REQUEST)
    
    print("H"*50)
    print("K"*50)
    if not days_exercises:
        return Response(
            {"detail": "At least one day of exercises must be provided"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
  # انشاء البرنامج
    program = Program.objects.create(
        coach=coach,
        trainer=trainer,
        description = request.data.get("description"),
    )
#تقسيم التمارين في البرنامج الى ايام وتكرارات ومجموعات
    for day_exercise in days_exercises:
        day = day_exercise.get("day")  
        sets = day_exercise.get("sets")  
        reps = day_exercise.get("reps")  
        exercises_ids = day_exercise.get("exercises", []) 

        if not exercises_ids:
             return Response({"detail": "Exercises must be provided for each day."}, status=status.HTTP_400_BAD_REQUEST)
        
        exercises = Exercise.objects.filter(exercise_id__in=exercises_ids)
        
        for exercise in exercises:
             ExerciseSchedule.objects.create(
                exercise=exercise,
                program=program,
                day=day,
                sets=sets,
                reps=reps
            )

    serialized_program = ProgramSerializer(program)
    return Response(serialized_program.data, status=status.HTTP_201_CREATED)
# ارجاع البرامج الصحية
@api_view(["GET"])
def get_program(request, user_id):
    trainer = get_object_or_404(Profile, user__id=user_id)
    program = Program.objects.filter(trainer=trainer).first()

    # إذا كان لا يوجد برنامج 
    if not program:
        return Response({}, status=status.HTTP_200_OK)

    schedules = ExerciseSchedule.objects.filter(program=program)
    exercises_with_days = []

    for schedule in schedules:
        exercise_info = {
            'day': schedule.day,
            'sets': schedule.sets,
            'reps' : schedule.reps,
            'exercise': ExerciseSerializer(schedule.exercise).data,
        }
        exercises_with_days.append(exercise_info)

    # إعداد البيانات للرد
    serialized_program = ProgramSerializer(program)
    response_data = serialized_program.data
    response_data['exercises'] = exercises_with_days  # إضافة التمارين مع الأيام

    return Response(response_data, status=status.HTTP_200_OK)

## لحذف برنامج رياضي لمتدرب محدد
@api_view(["DELETE"])
def delete_program(request,program_id,user_id):
#جلب المتدرب والبرنامج الذي نريد ان نحذفه
    deleter = get_object_or_404(Profile,user__id=user_id)
    program = get_object_or_404(Program,id=program_id)

    if(program and (program.coach==deleter or program.trainer==deleter)):
            program.delete()
            return(Response("Program Deleted Succesfuly"))
    else:
           return(Response("no program with that info"))

#يحدث كامل البرنامج
@api_view(["Post"])
def update_program(request,coach_id,program_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    print(coach.user.username)
    program = get_object_or_404(Program,id=program_id)

    days_exercises = request.data.get("days_exercises", [])

    if not days_exercises:
        return Response({"detail": "Days and exercises must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    

    if coach!=program.coach:
        print(program.coach.user.id)
        print(coach_id)
        return Response({"detail":"You Cant update on this program"})
    
    # حذف التمارين القديمة
    ExerciseSchedule.objects.filter(program=program).delete()

    for day_exercise in days_exercises:
        day = day_exercise.get("day")
        sets = day_exercise.get("sets")  
        reps = day_exercise.get("reps")
        exercises_ids = day_exercise.get("exercises", [])

        if not exercises_ids:
            return Response({"detail": f"At least one exercise must be provided for day {day}."}, status=status.HTTP_400_BAD_REQUEST)
#جلب التمارين التي وضعناها في البرنامج من الداتا بيز
        exercises = Exercise.objects.filter(exercise_id__in=exercises_ids)
        print("K"*50)

        if exercises.count() != len(exercises_ids):
            return Response(
                {"detail": "One or more exercises not found."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
        for exercise in exercises:
            ExerciseSchedule.objects.create(
                program=program,
                day=day,
                sets=sets, 
                reps=reps,
                exercise=exercise
            )
            
    serialized_program = ProgramSerializer(program)
    return Response(serialized_program.data, status=status.HTTP_200_OK)

#يحدث البرنامج من خلال التحديثات فقط ويبقي على الأيام التي لاتتغير
@api_view(["POST"])
def update_program_by_days(request, coach_id, program_id):
    coach = get_object_or_404(Profile, user__id=coach_id)
    program = get_object_or_404(Program, id=program_id)

    days_exercises = request.data.get("days_exercises", [])
    print(days_exercises)

    if not days_exercises:
        return Response({"detail": "Days and exercises must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    if coach != program.coach:
        return Response({"detail": "You can't update this program."})
  
    existing_days = list(ExerciseSchedule.objects.filter(program=program).values_list('day', flat=True))
    print(existing_days)

    for day_exercise in days_exercises:
        day = day_exercise.get("day")
        sets = day_exercise.get("sets")
        reps = day_exercise.get("reps")
        exercises_ids = day_exercise.get("exercises", [])
        print( {day})

        if not exercises_ids:
            return Response({"detail": f"At least one exercise must be provided for day {day}."}, status=status.HTTP_400_BAD_REQUEST)
        print(f"dd: {day},ex {existing_days}")

        exercises = Exercise.objects.filter(exercise_id__in=exercises_ids)
        
        if exercises.count() != len(exercises_ids):
            return Response({"detail": "One or more exercises not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        #اذا كان اليوم موجود في البرنامج يتم تحديثه كاملا حيث يحذف التمارين السابقة
        if str(day) in existing_days:
            print(f"Deleting exercises for {day}")
            ExerciseSchedule.objects.filter(program=program, day=day).delete()
            

        # نضيف التمارين واليوم 
        for exercise in exercises:
            ExerciseSchedule.objects.create(
                program=program,
                day=day,
                sets=sets, 
                reps=reps ,
                exercise=exercise
                )
    
    program.refresh_from_db()    
    serialized_program = ProgramSerializer(program)
    
    return Response(serialized_program.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_coach_programs(request,coach_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    programs = Program.objects.filter(coach=coach)

    serializer = ProgramSerializer(programs,many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_exercises_by_muscle(request):
    query = request.query_params.get('q', None)  
    if query:
        exercises = Exercise.objects.filter(muscle_group__icontains=query)  
    else:
        exercises = Exercise.objects.all()  

    serializer = ExerciseSerializer(exercises, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_exercise_list(request):
    exercises_data = request.data
    created_exercises = []

    for exercise in exercises_data:
        try:
            obj, created = Exercise.objects.update_or_create(
                exercise_id=exercise.get('exercise_id'),
                defaults={
                    'name': exercise.get('name'),
                    'muscle_group': exercise.get('muscle_group'),
                    'description': exercise.get('description', '')
                }
            )
            created_exercises.append({
                'exercise_id': obj.exercise_id,
                'created': created
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Exercises processed successfully.', 'results': created_exercises}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def recommend_program_ai(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    # عدم وضع برنامج ثاني اذا كان لدى المتدرب برنامج
    existing_program = Program.objects.filter(trainer=profile).first()
    if existing_program:
        return Response({
            'message': 'User already has an existing program.',
            'program_id': existing_program.id
        }, status=status.HTTP_400_BAD_REQUEST)
    
    #جلب الأمراض من الداتا بيز
    illnesses = list(IllnessToAvoidExercises.objects.all())
    illness_id = {ill.id: idx for idx, ill in enumerate(illnesses)}

    
   #معلومات المتدرب
    weight = profile.weight
    height = profile.height
    gender = encode_gender(profile.gender)
    level = encode_fitness_level(profile.experianse_level)
    goal = encode_goal(profile.goal) 
    illnesses = encode_illnesses(profile.illnesses, illness_id, len(illnesses))
  

    # تحميل المودل
    model = joblib.load('program_recommender_multi.joblib')
    mlb = joblib.load('exercise_mlb.joblib')

    #  مصفوفة التمارين المتوقعة
    X_basic = [weight, height, level, goal, gender]
    X = np.array([X_basic + illnesses])
    predicted = model.predict(X)
    exercise_ids = mlb.inverse_transform(predicted)[0]  # List of IDs

    # جلب تمارين
    exercises = list(Exercise.objects.filter(exercise_id__in=exercise_ids))
    print(exercises)


#المدرب الافتراضي
    virtual_coach = Profile.objects.get(user__username='ai_trainer') 
    print(virtual_coach)

    new_program = Program.objects.create(
        description="AI Generated Program",
        coach=virtual_coach,
        trainer=profile,
    )
#من اجل كل يوم سيعرض لنا ثلاث تمارين بكل يوم من ايام الاسبوع
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    exercisesinday = 3
    total = exercisesinday * len(days)

    if len(exercises) < total:
        exercises = random.choices(exercises, k=total)
    else:
        exercises = random.sample(exercises, total)
    #لإضافة البرنامج لجدول البرنامج في الداتا
    for i, day in enumerate(days):
        exercise1 = exercises[i * exercisesinday : (i + 1) * exercisesinday]

        for exercise in exercise1:
            if not ExerciseSchedule.objects.filter(program=new_program, exercise=exercise, day=day).exists():
              ExerciseSchedule.objects.create(
                  program=new_program,
                  exercise=exercise,
                  day=day,
                  sets=3 if profile.experianse_level == 'beginner' else 4,
                  reps=12 if profile.goal == 'build_muscle' else 15,
              )

    serializer = ProgramSerializer(new_program)
    return Response(serializer.data)

# Helper Encodings
def encode_fitness_level(level):
    return {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(level, 0)

def encode_goal(goal):
    return {'lose_weight': 0, 'build_muscle': 1, 'endurance': 2}.get(goal, 0)

def encode_gender(gender):
    return {'male': 0, 'female': 1}.get(gender, 0)

#تحويل الأمراض الى قائمة اعداد 0 اذا لم يكن موجود و 1 اذا كان المرض موجود
def encode_illnesses(user_illness, illness_id, list_length):
    list = [0] * list_length
    if not user_illness:
        return list
    for ill_id in user_illness:
        idx = illness_id.get(ill_id)
        if idx is not None:
            list[idx] = 1
    return list

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET"])
def get_exercises_with_avoid_flag(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    illnesses = profile.illnesses  

    all_exercises = Exercise.objects.all()
    avoid_exercise_names = set()

   
    avoid_entries = IllnessToAvoidExercises.objects.filter(illness__in=illnesses)
    for entry in avoid_entries:
        avoid_exercise_names.update(entry.exercise_to_avoid)

    result = []
    for exercise in all_exercises:
        result.append({
            "exercise_id": exercise.exercise_id,
            "name": exercise.name,
            "muscle_group": exercise.muscle_group,
            "description": exercise.description,
            "avoid": "yes" if exercise.name in avoid_exercise_names else "no"
        })

    return Response(result, status=status.HTTP_200_OK)

#لعرض التمارين حسب العضلة
@api_view(["GET"])
def get_exercises_with_avoid_flag_by_muscle(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    illnesses = profile.illnesses

    # أسم التمرين الذي يجب تجنبه حسب الأمراض
    avoid_exercise_names = set()
    avoid_entries = IllnessToAvoidExercises.objects.filter(illness__in=illnesses)
    for entry in avoid_entries:
        avoid_exercise_names.update(entry.exercise_to_avoid)

    #لجلب التمارين مصنفة حسب العضلة
    grouped_exercises = {}

    all_exercises = Exercise.objects.all()
    for exercise in all_exercises:
         muscle = exercise.muscle_group
         if muscle not in grouped_exercises:
            grouped_exercises[muscle] = []  # إنشاء قائمة جديدة للعضلة

         grouped_exercises[exercise.muscle_group].append({
            "exercise_id": exercise.exercise_id,
            "name": exercise.name,
            "description": exercise.description,
            "avoid": "yes" if exercise.name in avoid_exercise_names else "no"
         })

    return Response(grouped_exercises, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise
from .serializers import ExerciseSerializer

@api_view(["POST"])
def add_exercise_with_video(request):
    name = request.data.get("name")
    muscle_group = request.data.get("muscle_group")
    description = request.data.get("description")
    video_url = request.data.get("video_url")

    exercise = Exercise.objects.create(
        name=name,
        muscle_group=muscle_group,
        video_url=video_url,
        description=description,
    )
    exercise.save()
    return Response(ExerciseSerializer(exercise).data, status=status.HTTP_201_CREATED)
