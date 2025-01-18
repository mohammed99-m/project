from django.urls import path
from .views import  list_exercises, search_exercises

urlpatterns = [
   path('listexercises/',list_exercises,name="List Of Exercises"),
   path('searchexercises/',search_exercises,name="Search About Exercise")
]