from django.urls import path
from .views import  list_exercises, search_exercises ,make_program , get_program ,delete_program , update_program , get_coach_programs, update_program_by_days

urlpatterns = [
   path('listexercises/',list_exercises,name="List Of Exercises"),
   path('programs/<int:user_id>/', get_program, name='get_program'),
   path('searchexercises/',search_exercises,name="Search About Exercise"),
   path('makeprogram/<str:coach_id>/<str:trainer_id>/',make_program,name="make program"),
   path('gettrainerprogram/<str:user_id>/',get_program,name="Get Trainer's Program"),
   path('deleteprogram/<str:program_id>/<str:user_id>/',delete_program,name="Delete Program"),
   path('updateprogram/<str:coach_id>/<str:program_id>/',update_program,name="Update Program"),
   path('updateprogrambydays/<str:coach_id>/<str:program_id>/',update_program_by_days,name="Update Program by days"),
   path('getcoachprograms/<str:coach_id>/',get_coach_programs,name="Get Coach's Programs")
]