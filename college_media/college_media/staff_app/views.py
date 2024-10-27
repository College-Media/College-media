from django.shortcuts import render,redirect # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from staff_app.models import *
from django.contrib import messages # type: ignore
# Create your views here.
from django.shortcuts import get_object_or_404
def welcome(request):
    return render(request,"welcome.html")
def add_student(request):
    
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        dob=request.POST.get('dob')
        roll_num=request.POST.get('roll')
        section=request.POST.get('section')
        school_name=request.POST.get('class')
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
            custom_user_instance = get_object_or_404(CoustomUser, username=roll_num)
            print(custom_user_instance)
            student_add=Student.objects.create(user=custom_user_instance,roll_number=roll_num,name=name,email=email,section=section,school=school_name,dob=dob)
            messages.success(request,"student added success")
            redirect("staff_dash/add_student/")
    return render(request,"staff_pages/add_students.html")

def home(request):
    return render(request,"staff_pages/staf_home.html")