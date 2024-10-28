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
                    login(request,user)
                    return redirect("user_dash/home/")
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

def maheshaa():
    subject = 'Welcome to our website'    
    message = 'Thank you for registering at our site.'
    recipient_list = ['aradhyashetty74@gmail.com','adithyamaiyam.2002@gmail.com']  # The recipient’s email
    email_from = settings.DEFAULT_FROM_EMAIL    
    send_mail(subject, message, email_from, recipient_list) # type: ignore

def profile(request):
    user=request.user
    users=CoustomUser.objects.get(username=user)
    if users.is_staff:
        return render(request,"staff_pages/staff_profile.html")
    else:
        return render(request,"profile.html")


def password_reset(request):
    return render(request,"forgot-password.html")

def logout_user(request):
    logout(request)
    return render(request,"login.html")

def search_student(request):
    user=request.user
    users=CoustomUser.objects.get(username=user)
    if request.method == "POST":
        roll_number = request.POST.get("roll_number")  # Retrieve the roll number from the form        
        try:          
            # Attempt to find a student with the provided roll number
            student = Student.objects.filter(roll_number__icontains=roll_number)
            if student:
                if users.is_staff:
                    return render(request,"staff_pages/staff_search_page.html",{'student':student})
                else:
                    return render(request, "search.html", {'student': student})  
            else:
                if users.is_staff:
                        return render(request,"staff_pages/staff_search_page.html",{'message': "No student found with this roll number."})
                else:
                        return render(request, "search.html", {'message': "No student found with this roll number."})     
        
        except Student.DoesNotExist:
            if users.is_staff:
                return render(request,"staff_pages/staff_search_page.html",{'message': "No student found with that roll number."})
            else:
                return render(request, "search.html", {'message': "No student found with that roll number."})             

    # If the request is GET, simply render the form without any student data
    
    if users.is_staff:
         return render(request,"staff_pages/staff_search_page.html")
    else:
        return render(request, "search.html")
        
        
import random  
def reset_password(request):
    if request.method=="POST":
        btn=request.POST.get('btn')
        if btn=='1':
            request.session["a"]=str(random.randrange(1000,9999))
            print(request.session["a"])
            
        if btn=='1':
                mail=request.POST.get('mail')
                print(mail)
                is_exists=CoustomUser.objects.filter(email=mail)
                request.session['email']=mail
                if is_exists:
                    
                   subject = "College_media | OTP"
                   message = f"Hi, your one-time password is: {request.session['a']}"
                   recipient_list = [mail]  # The recipient’s email
                   email_from = settings.DEFAULT_FROM_EMAIL

                   send_mail(subject, message, email_from, recipient_list)
                    # message =f"hi your one time password is:"+request.session['a']
                    # email_from =settings.EMAIL_HOST_USER
                    # recipient_list=[mail]
                    # send_mail(subject1,message,email_from,recipient_list) # type: ignore
                   return render(request,'reset_password.html',{'type':2})
                else:
                    messages.success(request,"email not exists ")
                    return render(request,'reset_password.html',{'type':1}) 
        elif btn=='2':
                otp=request.POST.get('otp')
                print(otp)
                a=request.session['a']
                
                if otp==a:
                  return render(request,'reset_password.html',{'type':3})  
                else:
                    messages.success(request,"please enter the correct otp")
                    return render(request,'reset_password.html',{'type':2}) 
        else:
               pas=request.POST.get('pas')
               cpas=request.POST.get('cpas')
               if pas==cpas:
                    mail=request.session['email']
                    user=CoustomUser.objects.get(email=mail)
                    user.set_password(pas)
                    user.save()
                    return redirect("login")
               else:
                    messages.success(request,"enter the password correctly")
                    return render(request,'reset_password.html',{'type':3}) 
    return render(request,'reset_password.html',{'type':1})