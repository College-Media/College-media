from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from staff_app.models import *
from django.contrib import messages
# Create your views here.
def welcome(request):
    return render(request,"welcome.html")
def add_student(request):
    
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        dob=request.POST.get('dob')
        roll_num=request.POST.get('roll')
        section=request.POST.get('dob')
        class_name=request.POST.get('dob')
        print(name,email)
        s=CoustomUser.objects.filter(username=roll_num)
        print(s)
        if s:
            messages.error(request,"student already exists")
            redirect("staff_dash/add_student/")
        else:
            user=CoustomUser.objects.create_user(roll_num,email,dob)
            user.is_student=True
            user.save()
            messages.success(request,"student added success")
            redirect("staff_dash/add_student/")
    return render(request,"staff_pages/add_students.html")