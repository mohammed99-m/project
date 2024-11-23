from django.urls import path
from .views import NameView

urlpatterns = [
    path('names/', NameView.as_view(), name='name-list'),
]