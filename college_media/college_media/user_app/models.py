from django.db import models
from django.db import models
from django.contrib.auth.models import User
from staff_app.models import *



class Post(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)    
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student.name

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="likes_given",null="True")


    def __str__(self):
        return self.student.roll_number

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


# Create your models here.
