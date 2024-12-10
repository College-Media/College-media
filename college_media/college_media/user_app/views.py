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
    print(request.user.roll_number)
    liked_by=Student.objects.get(roll_number=request.user.roll_number)    
    liked_post_ids = Like.objects.filter(liked_by=liked_by).values_list('post_id', flat=True)
    likes=Like.objects.all()
    commets=Comment.objects.all()
    context=Student.objects.get(roll_number=request.user)
    print(context)
    return render(request,"user_pages/user_home.html",{'posts':posts,'liked_post_ids': set(liked_post_ids),'likes':likes,'coments':commets,'context':context})

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
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'username':
            username = request.POST['name']
            student_info.name = username
            student_info.save()
            messages.success(request, "User Name Updated", extra_tags='username')
        elif form_type == 'profile_pic':
            if 'img' in request.FILES:
                image_file = request.FILES['img']
                student_info.profile_image = image_file
                student_info.save()
                messages.success(request, "Profile Picture Updated", extra_tags='profile_pic')
            else:
                messages.error(request, "No image file provided.", extra_tags='profile_pic')
    return render(request,"user_pages/user_profile.html",{'student_info':student_info,'posts':post})
    
