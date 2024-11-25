from django.shortcuts import render,redirect
from user_app.models import *
from staff_app.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Student
from django.contrib import messages # type: ignore
from django.utils.timezone import now
from datetime import timedelta
# Create your views here.
def welcome(request):
    return render(request,"home.html")

def home(request):
    last_24_hours = now() - timedelta(hours=24)
    # posts= Post.objects.filter(created_at__gte=last_24_hours, is_approved=True)
    posts = Post.objects.select_related('student').filter(is_approved=True).order_by('-created_at')  # Use select_related to fetch related student data efficiently
    return render(request,"user_pages/user_home.html",{'posts':posts})

def add_post(request):
    if request.method=='POST':
        # title=request.POST['title']
        body=request.POST['body']
        img=request.FILES['img']
        user=request.user
        student_instence=get_object_or_404(Student, user=user)
        posts=Post.objects.create(student=student_instence,content=body,image=img ,is_approved=False)
        posts.save()
        # print(title,body)
        messages.success(request,"post sent for verification")
        return redirect('/user_dash/add_post')    
    return render(request,"user_pages/add_post.html")

def user_profile(request):
    user=request.user
    student_info=Student.objects.get(user=user) 
    post=Post.objects.filter(student__roll_number=student_info.user)
    comments=Comment.objects.filter(student__roll_number=student_info.user)     
    for i in post:
        print(i.id)
    return render(request,"user_pages/user_profile.html",{'student_info':student_info,'posts':post})
