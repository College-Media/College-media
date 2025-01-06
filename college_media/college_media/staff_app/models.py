from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models her

class CoustomUser(AbstractUser):
    is_student=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    roll_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    def __str__(self):
        return self.username
    
class Student(models.Model):
    user = models.OneToOneField(CoustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    name=models.CharField(max_length=30, blank=True)
    section=models.CharField(max_length=10, blank=True)
    school=models.CharField(max_length=100, blank=True)
    dob=models.CharField(max_length=20, blank=True)
    profile_image=models.ImageField(upload_to='profile_image/', blank=True, null=True)
    
    def __str__(self):
        return self.roll_number
    
    
class Main_Notifications(models.Model):
    sender=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="sent_notification")
    receiver=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="received_notification")
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    content=models.TextField(blank=True)
    
    
    def __str__(self) :
        return f"{self.sender}-{self.receiver}-{self.is_read}-{self.created_at}"