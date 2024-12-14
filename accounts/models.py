from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=15,blank=True,null=True)
    goal = models.CharField(max_length=15,blank= True ,null = True)
    experianse_level = models.CharField(max_length= 15 ,blank=True,null=True)
    user_type = models.CharField(max_length= 15 ,blank=True,null=True) 


    def __str__(self):
        return self.user.username
    