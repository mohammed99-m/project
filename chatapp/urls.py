from django.urls import path
from .views import get_messages, save_message

urlpatterns = [
    path("save-message/", save_message, name="save-message"),
    path("get-message/<str:room_name>/", get_messages, name="get-message"),

]