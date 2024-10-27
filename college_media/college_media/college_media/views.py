from django.shortcuts import render,redirect
from django.core.mail import send_mail # type: ignore
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from staff_app.models import *

# Create your views here.
def home(request):
        # if not request.user.is_anonymous:
        #     if request.session['remember']=='1':
        #         user=request.user
        #         if user.is_student:
        #             login(request,user)
        #             return redirect('user_dash/home')
        #         elif user.is_staff:
        #             login(request,user)
        #             return redirect("staff_dash/add_student/")
        print("login page")
                
        if request.method=="POST":
            name=request.POST.get('roll')
            pass1=request.POST.get('password')
            print(name ,pass1)
            # remember=request.POST['rem']/
            request.session['remember']='1'
            user=authenticate(username=name,password=pass1)
            print(user)          
            if user:
                p=CoustomUser.objects.get(username=user)
                if p.is_staff:
                    login(request,user)
                    redirect("staff_dash/add_student/")
                elif p.is_student:
                    login(request,user)
                    redirect("staff_dash/add_student/")
                else:
                    return render(request,'login.html')
                # if user is not None:
                #     if user.is_staff:
            #         # request.session['messege']='admin'
            #         login(request,user)
                    
            #         p=CoustomUser.objects.filter(username=user)
            #         return render(request,"home.html")
            #     elif user.is_student:
            #         # request.session['messege']='s_p'
            #         login(request,user)
            #         redirect("staff_dash/add_student/")
            #     else:
            #         return render(request,"user.html")
            # else:
            #     messages.warning(request,"please enter correct email and password")
            #     return render(request,'login.html')
        return render(request,'login.html')

def login_page(request):
     # if not request.user.is_anonymous:
        #     if request.session['remember']=='1':
        #         user=request.user
        #         if user.is_student:
        #             login(request,user)
        #             return redirect('user_dash/home')
        #         elif user.is_staff:
        #             login(request,user)
        #             return redirect("staff_dash/add_student/")
        print("login page")
                
        if request.method=="POST":
            name=request.POST.get('roll')
            pass1=request.POST.get('password')
            print(name ,pass1)
            # remember=request.POST['rem']/
            request.session['remember']='1'
            user=authenticate(username=name,password=pass1)
            print(user)
          
            if user is not None:
                p=CoustomUser.objects.get(username=user)
                print(p)
                print(p.is_staff)
                print(p.is_student)
                if p.is_staff:
                    login(request,user)
                    messages.success(request,'Login successfull')
                    return render(request,"staff_pages/staf_home.html")
                elif p.is_student:
                    print("hello there")
                    login(request,user)
                    return render(request,"home.html")
                else:
                    return render(request,'login.html')
                # if user is not None:
                #     if user.is_staff:
            #         # request.session['messege']='admin'
            #         login(request,user)                    
            #         p=CoustomUser.objects.filter(username=user)
            #         return render(request,"home.html")
            #     elif user.is_student:
            #         # request.session['messege']='s_p'
            #         login(request,user)
            #         redirect("staff_dash/add_student/")
            #     else:
            #         return render(request,"user.html")
            # else:
            #     messages.warning(request,"please enter correct email and password")
            #     return render(request,'login.html')         
        return render(request,'login.html')

def send_mail():
    subject = 'Welcome to our website'    
    message = 'Thank you for registering at our site.'
    recipient_list = ['aradhyashetty74@gmail.com','adithyamaiyam.2002@gmail.com']  # The recipient’s email
    email_from = settings.DEFAULT_FROM_EMAIL    
    send_mail(subject, message, email_from, recipient_list) # type: ignore

def profile(request):
    return render(request,"profile.html")


def password_reset(request):
    return render(request,"forgot-password.html")

def logout_user(request):
    logout(request)
    return render(request,"login.html")

def search_student(request):
    user=request.user
    users=CoustomUser.objects.get(username=user)
    search_student=request.POST.get("roll_number")
    if users.is_staff:
        return render(request,"staff_pages/staff_search_page.html")
    else:
        return render(request,"search.html")
     
        
    #     student=Student.objects.all()
    #     print(student)
    #     # for stu in student:
    #     #     if stu.roll_number==search_student:
    #     #         print("Student found")
    #     #         break
    #     #     else:
    #     #         print("Student not found")
    #  return render(request,"search.html")