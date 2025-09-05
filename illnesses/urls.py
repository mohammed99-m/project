from django.urls import path
from .views import get_exercises_to_avoid_for_user, get_foods_to_avoid_for_user, list_illnesses,add_illnisses_list,add_illnisses_exercises_list,list_illnesses_exercises,delete_all_illnesses,force_delete_illnesses_exercises,force_delete_illnesses_food

urlpatterns = [
    path('deleteillness',delete_all_illnesses,name='delete all illness'),
    path('illnesses/', list_illnesses, name='list_illnesses'),
    path('addillnesses/',add_illnisses_list,name="add Illnesses"),
    path('illnesses_exercises/', list_illnesses_exercises, name='list_illnesses_exercises'),
    path('addillnesses_exercises/',add_illnisses_exercises_list,name="add Illnesses Exercises"),
    path('illnessesexercisesavoid/<int:user_id>/', get_exercises_to_avoid_for_user, name='get_exercises_to_avoid_for_user'),
    path('illnessesfoodsavoid/<int:user_id>/', get_foods_to_avoid_for_user, name='get_food_to_avoid_for_user'),
    path('force_delete_illnesses_food/<str:illnesses_id>/',force_delete_illnesses_food,name="delete illnesses food by force"),
    path('force_delete_illnesses_exercises/<str:illnesses_id>/',force_delete_illnesses_exercises,name='delete illnesses exercises by force')
]