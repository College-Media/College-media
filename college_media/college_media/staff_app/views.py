from django.shortcuts import render,redirect # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from staff_app.models import *
from user_app.models import *
from django.contrib import messages # type: ignore
# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail # type: ignore
from django.conf import settings
# code for sending main
def mail_send(subject,message,mail):
    recipient_list = [mail]  # The recipient’s email
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, email_from, recipient_list)
    
    
    
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
    posts = Post.objects.select_related('student').filter(is_approved=True)  # Use select_related to fetch related student data efficiently
    print(posts)
    return render(request,"staff_pages/staf_home.html",{'posts':posts})

def option_student_add(request):
    return render(request,"staff_pages/add_student_option.html")

def staff_post_request(request):
    post=Post.objects.select_related('student').filter(is_approved=False )    
    return render(request,"staff_pages/staff_post_request.html",{"posts":post})


def approve_or_reject_post(request):
    if request.method=="POST":
        
        accept= request.POST.get('accept')
        reject=request.POST.get('reject')
        
        print(accept,reject)
        if accept:  
            post=get_object_or_404(Post,id=accept)
            post.is_approved=True
            post.save()
            subject="College Media:Post Acceptence from staff post on{}".format(post.created_at)
            message="Your post is accepted "
            mail=post.student.email
            mail_send(subject,message,mail)
            return redirect('/staff_dash/staff_post_request')
        elif reject:
            post=get_object_or_404(Post,id=reject)
            subject="College Media:{} Post Rejected from staff post on{}".format(post.student.name,post.created_at)
            message="Your post is Rejected "
            mail=post.student.email
            mail_send(subject,message,mail)
            post.delete()
            return redirect('/staff_dash/staff_post_request')
    return redirect('/staff_dash/staff_post_request')        

def staff_profile(request):
    user=request.user
    student_info=Student.objects.get(user=user)     
    return render(request,"staff_pages/staff_profile.html",{'student_info':student_info})

