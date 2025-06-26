
from django.urls import path
from .views import  list_exercises, recommend_program_ai, search_exercises ,make_program , get_program ,delete_program , update_program , get_coach_programs, update_program_by_days,get_exercises_with_avoid_flag,add_exercise_with_video
from .views import  get_exercises_by_muscle, list_exercises, search_exercises ,make_program , get_program ,delete_program, update_program , get_coach_programs, update_program_by_days,add_exercise_list,get_exercises_with_avoid_flag_by_muscle

urlpatterns = [
   path('listexercises/',list_exercises,name="List Of Exercises"),
   path('programs/<str:user_id>/', get_program, name='get_program'),
   path('searchexercises/',search_exercises,name="Search About Exercise"),
   path('by-muscle/',get_exercises_by_muscle,name="get exercises"),
   path('makeprogram/<str:coach_id>/<str:trainer_id>/',make_program,name="make program"),
   path('coachprograms/<str:coach_id>/',get_coach_programs,name='coach progrmas'),
   path('gettrainerprogram/<str:user_id>/',get_program,name="Get Trainer's Program"),
   path('deleteprogram/<str:program_id>/<str:user_id>/',delete_program,name="Delete Program"),
   path('updateprogram/<str:coach_id>/<str:program_id>/',update_program,name="Update Program"),
   path('updateprogrampyday/<str:coach_id>/<str:program_id>/',update_program_by_days,name="Update Program By Days"),
   path('add-exercises/', add_exercise_list, name='add-exercise-list'),
   path('add-exercise-with-video/', add_exercise_with_video, name='add-exercise-with-video'),
   path('ai-program/<str:user_id>/', recommend_program_ai, name='ai_program'),
   path('avoidexercises/<str:user_id>/',get_exercises_with_avoid_flag,name='avoided exercises'),
   path('avoidexercisesbymuscle/<str:user_id>/',get_exercises_with_avoid_flag_by_muscle,name="Avoid Exercises by Muscle"),
 
]