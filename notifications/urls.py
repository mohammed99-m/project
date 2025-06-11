from django.urls import path
from .views import get_user_notifications, save_notification

urlpatterns = [
    path('save-notification/', save_notification, name='save-notification'),
    path('user-notifications/<int:user_id>/', get_user_notifications, name='user-notifications'),

]