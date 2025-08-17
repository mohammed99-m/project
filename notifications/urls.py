from django.urls import path
from .views import get_user_notifications, save_notification,save_notification2

urlpatterns = [
    path('save-notification/', save_notification, name='save-notification'),
    path('save-notification2/', save_notification2, name='save-notification'),
    path('user-notifications/<str:receiver_id>/', get_user_notifications, name='user-notifications'),

]