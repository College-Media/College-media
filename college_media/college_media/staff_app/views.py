from django.shortcuts import render,redirect # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from staff_app.models import *
from user_app.models import *
from django.contrib import messages # type: ignore
# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail # type: ignore
from django.conf import settings
from openpyxl import load_workbook #toload excl file
import os

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
        s=CoustomUser.objects.filter(username=roll_num)
        if s:
            messages.error(request,"student already exists")
            redirect("staff_dash/add_student/")
        else:
            user=CoustomUser.objects.create_user(roll_num,email,dob)
            user.roll_number=roll_num
            user.is_student=True
            user.save()
            custom_user_instance = get_object_or_404(CoustomUser, username=roll_num)
            print(custom_user_instance)
            student_add=Student.objects.create(user=custom_user_instance,roll_number=roll_num,name=name,email=email,section=section,school=school_name,dob=dob)
            messages.success(request,"student added success")
            redirect("staff_dash/add_student/")
    return render(request,"staff_pages/add_students.html")


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


def add_students(request):
    if request.method == "POST":
        # Check if a file is uploaded
        if 'file' not in request.FILES or not request.FILES['file']:
            messages.error(request, "No file uploaded.")
            return redirect("/staff_dash/add_students")

        # Get the uploaded file
        uploaded_file = request.FILES['file']

        # Save the file temporarily
        path = f"/tmp/{uploaded_file.name}"
        print(uploaded_file)
        # Process the file (read Excel and save data to the database)
        try:
            workbook = load_workbook(filename=path)
            sheet = uploaded_file.active  # Assuming data is in the first sheet
            print(sheet)
            # Loop through rows in the Excel file
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip the header row
                roll_number, email, name, section, school_name, dob, profile_image = row

                # Create CoustomUser
                user = CoustomUser.objects.create_user(
                    username=roll_number,  # Assuming username is roll_number
                    email=email,
                    password=dob  # Using DOB as a temporary password; update as needed
                )
                user.roll_number = roll_number
                user.is_student = True
                user.save()

                # Create Student
                Student.objects.create(
                    user=user,
                    roll_number=roll_number,
                    name=name,
                    email=email,
                    section=section,
                    school=school_name,
                    dob=dob
                    # profile_image=profile_image  # Ensure this is handled appropriately
                )

            messages.success(request, "Students added successfully.",extra_tags='student_add')
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

        # Clean up: Remove the temporary file
        # os.remove(file_path)
        return redirect("/staff_dash/add_students")

    return render(request,"staff_pages/add_multiple_student.html")