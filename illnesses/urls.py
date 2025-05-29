from django.urls import path
from .views import list_illnesses,add_illnisses_list,add_illnisses_exercises_list,list_illnesses_exercises,delete_all_illnesses

urlpatterns = [
    path('deleteillness',delete_all_illnesses,name='delete all illness'),
    path('illnesses/', list_illnesses, name='list_illnesses'),
    path('addillnesses/',add_illnisses_list,name="add Illnesses"),
    path('illnesses_exercises/', list_illnesses_exercises, name='list_illnesses_exercises'),
    path('addillnesses_exercises/',add_illnisses_exercises_list,name="add Illnesses Exercises"),
]