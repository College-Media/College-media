from django.shortcuts import render,redirect
from user_app.models import *
from staff_app.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Student
from django.contrib import messages # type: ignore
# Create your views here.
def welcome(request):
    return render(request,"home.html")

def home(request):
    posts = Post.objects.select_related('student').filter(is_approved=True)  # Use select_related to fetch related student data efficiently
    print(posts)
    return render(request,"user_pages/user_home.html",{'posts':posts})

def add_post(request):
    if request.method=='POST':
        title=request.POST['title']
        body=request.POST['body']
        img=request.FILES['img']
        user=request.user
        student_instence=get_object_or_404(Student, user=user)
        posts=Post.objects.create(student=student_instence,content=body,image=img ,is_approved=False)
        posts.save()
        print(title,body)
        print("hello there")
        messages.success(request,"post sent for verification")
        return redirect('/user_dash/add_post')
    
    return render(request,"user_pages/add_post.html")

def user_profile(request):
    user=request.user
    student_info=Student.objects.get(user=user)     
    return render(request,"user_pages/user_profile.html",{'student_info':student_info})
