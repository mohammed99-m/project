from django.urls import path
from .views import sign_up ,login , delete_account ,test_token
urlpatterns = [
    path('register/',sign_up, name='Register'),
    path('login/',login,name='Login'),
    path('delete/',delete_account,name="Delete"),
    path('getInfo/',test_token,name="GET Informations")

]