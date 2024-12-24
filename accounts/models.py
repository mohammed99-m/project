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
    ## علاقة التدريب
    trainers = models.ManyToManyField(
        'self',
        symmetrical=False,  # Ensure the relationship is directional
        related_name='related_to',
        blank=True
    )
    def __str__(self):
        return self.user.username
## جدول يدل على الطلبات 
class JoinRequest(models.Model):
    trainer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_requests')  
    coach = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_requests') 
    ## حالة الطلب
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.user.user.username} to {self.coach.user.username} ({self.status})"

    


