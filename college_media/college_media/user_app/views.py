from django.shortcuts import render,redirect
from user_app.models import *
from staff_app.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Student
from django.contrib import messages # type: ignore
from django.utils.timezone import now
from datetime import timedelta
import random
# Create your views here.
def welcome(request):
    return render(request,"home.html")

def home(request):    
    posts = Post.objects.select_related('student').order_by('?') 
    liked_by=Student.objects.get(roll_number=request.user)    
    liked_post_ids = Like.objects.filter(liked_by=liked_by).values_list('post_id', flat=True)
    likes=Like.objects.all()
    return render(request,"user_pages/user_home.html",{'posts':posts,'liked_post_ids': set(liked_post_ids),'likes':likes})

def add_post(request):
    if request.method=='POST':
        body=request.POST['body']
        img=request.FILES['img']
        user=request.user
        student_instence=get_object_or_404(Student, user=user)
        posts=Post.objects.create(student=student_instence,content=body,image=img ,is_approved=False)
        posts.save()
        messages.success(request,"post sent for verification")
        return redirect('/user_dash/add_post')    
    return render(request,"user_pages/add_post.html")

def user_profile(request):
    user=request.user
    student_info=Student.objects.get(user=user) 
    post=Post.objects.filter(student__roll_number=student_info.user)
    comments=Comment.objects.filter(student__roll_number=student_info.user) 
    if request.method =='POST':
        username=request.POST['name']
        student_info.name=username
        student_info.save()
    return render(request,"user_pages/user_profile.html",{'student_info':student_info,'posts':post})
    
