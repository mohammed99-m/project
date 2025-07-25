from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    illnesses = models.JSONField(default=list,null=True,blank=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=15,blank=True,null=True,
        choices=[('male', 'male'), ('female', 'female')],
        default='male')
    
    goal = models.CharField(max_length=15,blank= True ,null = True ,
        choices=[('lose_weight', 'lose_weight'), ('build_muscle', 'build_muscle'), ('endurance', 'endurance')],
        default='build_muscle')
    
    experianse_level = models.CharField(max_length= 15 ,blank=True,null=True,
        choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('advanced', 'advanced')],
        default='beginner')
    user_type = models.CharField(max_length= 15 ,blank=True,null=True,
        choices=[('coach', 'coach'), ('trainer', 'trainer')],
        default='trainer')
    ## علاقة التدريب
    trainers = models.ManyToManyField(
        'self',
        symmetrical=False,  # Ensure the relationship is directional
        related_name='related_to',
        blank=True
    )
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    player_id = models.CharField(blank=True,null=True,max_length=500)
    image_url = models.URLField(blank=True, null=True)
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



    


