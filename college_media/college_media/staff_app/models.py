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
    
    def __str__(self):
        return self.roll_number
    