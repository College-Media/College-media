from django.shortcuts import render,redirect # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from staff_app.models import *
from user_app.models import *
from chat_app.models import *
from django.contrib import messages # type: ignore
# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail # type: ignore
from django.conf import settings
# from openpyxl import load_workbook #toload excl file
import os
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# code for sending main
from django.db import IntegrityError
def mail_send(subject,message,mail):
    recipient_list = [mail]  # The recipient’s email
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, email_from, recipient_list)
    
    
    
def welcome(request):
    return render(request,"welcome.html")


def add_student(request):
    if request.method == "POST":
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        roll_num = request.POST.get('roll')
        section = request.POST.get('section')
        school_name = request.POST.get('class')
        tag = request.POST.get('tag')
        print(dob)
        
        # Check if student with the given roll number already exists in CoustomUser
        existing_user = CoustomUser.objects.filter(username=roll_num).exists()
        # Check if student with the given email already exists in Student or CoustomUser
        existing_email = CoustomUser.objects.filter(email=email).exists()
        existing_student_email = Student.objects.filter(email=email).exists()

        if existing_user:
            messages.error(request, "A student with this roll number already exists.", extra_tags='student_exists')
            print("Student already exists by roll number")
            return redirect("add_student")  # Redirect to the add_student page
        elif existing_email or existing_student_email:
            messages.error(request, "A student with this email already exists.", extra_tags='student_exists')
            print("Student already exists by email")
            return redirect("add_student")  # Redirect to the add_student page

        try:
            # Create a new user and student
            user = CoustomUser.objects.create_user(roll_num, email, dob)
            user.roll_number = roll_num
            user.is_student = True
            user.save()
            
            # Create student instance
            custom_user_instance = CoustomUser.objects.get(username=roll_num)
            Student.objects.create(
                user=custom_user_instance, roll_number=roll_num,
                name=name, email=email, section=section, school=school_name, dob=dob
            )
            
            # Send welcome email
            subject = "College Media: You are added to college media"
            html_content = render_to_string('email.html', {'roll_num': roll_num, 'name': name, 'dob': dob})
    
            # Optionally, create a plain-text version for email clients that don't support HTML
            plain_text_content = strip_tags(html_content)
            message = "Your login is: {} and your password is: {}".format(roll_num, dob)
            mail = email
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]  # The recipient’s email
            send_mail(
                subject, 
                plain_text_content,  
                email_from,
                recipient_list,
                html_message=html_content  # This is required for HTML content
            )
            
            # Create tag relation
            tag_giver = Student.objects.get(user=request.user)
            tag_reciver = Student.objects.get(user=user)
            Tag.objects.create(
                tag_given_by=tag_giver, tag_person=tag_reciver, tag=tag, universal=True
            )

            # Success message
            print("Student added successfully")
            messages.success(request, "Student added successfully", extra_tags='student_added')
            return redirect("add_student")  # Redirect to the add_student page

        except IntegrityError as e:
            # Catch IntegrityError (e.g., if roll_number or email is duplicated)
            messages.error(request, "An error occurred while adding the student. Please try again.", extra_tags='student_exists')
            print("IntegrityError: ", e)
            return redirect("add_student")  # Redirect to the add_student page

    return render(request, "staff_pages/add_students.html")


def home(request):
    posts = Post.objects.select_related('student').order_by('?') 
    liked_by=Student.objects.get(roll_number=request.user)    
    liked_post_ids = Like.objects.filter(liked_by=liked_by).values_list('post_id', flat=True)
    likes=Like.objects.all()   
    return render(request,"staff_pages/staf_home.html",{'posts':posts,'liked_post_ids': set(liked_post_ids),'likes':likes})

def option_student_add(request):
    return render(request,"staff_pages/add_student_option.html")

def staff_post_request(request):
    post=Post.objects.select_related('student').filter(is_approved=False )    
    return render(request,"staff_pages/staff_post_request.html",{"posts":post})


def approve_or_reject_post(request):
    if request.method=="POST":        
        accept= request.POST.get('accept')
        reject=request.POST.get('reject')
        
        if accept:  
            post=get_object_or_404(Post,id=accept)
            post.is_approved=True
            post.save()
            sender= get_object_or_404(Student,user=request.user)
            reciver=get_object_or_404(Student,roll_number=post.student.roll_number)
            Main_Notifications.objects.create(sender=sender,receiver=reciver,content="College Media:{} Post Accepted from staff post on{}".format(post.student.name,post.created_at))
            subject="College Media:Post Acceptence from staff post on{}".format(post.created_at)
            message="Your post is accepted "
            mail=post.student.email
            mail_send(subject,message,mail)
            messages.success(request, "post is accepted successfully", extra_tags='post_accepted')
            return redirect('/staff_dash/staff_post_request')
        elif reject:
            post=get_object_or_404(Post,id=reject)
            sender= get_object_or_404(Student,user=request.user)
            reciver=get_object_or_404(Student,roll_number=post.student.roll_number)
            Main_Notifications.objects.create(sender=sender,receiver=reciver,content="College Media:{} Post Rejected from staff post on{}".format(post.student.name,post.created_at))
            subject="College Media:{} Post Rejected from staff post on{}".format(post.student.name,post.created_at)
            message="Your post is Rejected "
            mail=post.student.email
            mail_send(subject,message,mail)
            post.delete()
            messages.success(request, "post is  rejected successfully", extra_tags='post_rejected')
            return redirect('/staff_dash/staff_post_request')
            
    return redirect('/staff_dash/staff_post_request')        

def staff_profile(request):
    user=request.user
    student_info=Student.objects.get(user=user)  
    post=Post.objects.filter(student__roll_number=student_info.user)
    if request.method =='POST':
        form_type = request.POST.get('form_type')
        if form_type == 'username':
            username=request.POST['name']
            student_info.name=username
            student_info.save()
        elif form_type == 'profile_pic':
            image_file = request.FILES['img']
            student_info.profile_image=image_file  # Create a new model instance
            student_info.save()  
    return render(request,"staff_pages/staff_profile.html",{'student_info':student_info,'posts':post})

import numpy as np # type: ignore
import pandas as pd

def add_students(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)        
        for index, row in df.iterrows():
                # Create Student
            s = CoustomUser.objects.filter(username=row['roll_num'])
            if s:
                messages.error(request, "Student already exists", extra_tags='student_add')
                print("student alredy exists")
                return redirect("staff_das/add_students")  # Redirect to the add_student page
            else:
                try:
            # Create new user and student
                    user = CoustomUser.objects.create_user(row['roll_num'],row['email'], row['dob'])
                    user.roll_number =row['roll_num'] 
                    user.is_student = True
                    user.save()
            
            # Create student instance
                    custom_user_instance = CoustomUser.objects.get(username=row['roll_num'])
                    Student.objects.create(
                        user=custom_user_instance,
                        roll_number=row['roll_num'],
                        name=row['name'],
                        email=row['email'],
                        section=row['section'],
                        school=row['school_name'],
                        dob=row['dob']
                # profile_image=profile_image  # Ensure this is handled appropriately
                    )

                    messages.success(request, "Students added successfully.")
                except Exception as e:
                     messages.error(request, f"Error processing file: {e}")
        return redirect("/staff_dash/add_students")

    return render(request,"staff_pages/add_multiple_student.html")

# def staff_post(request):