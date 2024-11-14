from django.shortcuts import render,redirect
from django.core.mail import send_mail # type: ignore
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from staff_app.models import *
from user_app.models import *
from django.http import JsonResponse #like 
from django.contrib.auth.decorators import login_required #comments

# Create your views here.
def home(request):
        return render(request,'login.html')

def login_page(request):
        if request.method=="POST":
            name=request.POST.get('roll')
            pass1=request.POST.get('password')
            # remember=request.POST['rem']/
            request.session['remember']='1'
            user=authenticate(username=name,password=pass1)
          
            if user is not None:
                p=CoustomUser.objects.get(username=user)
                if p.is_staff:
                    login(request,user)
                    messages.success(request,'Login successfull')
                    return redirect("staff_dash/home/")
                elif p.is_student:
                    login(request,user)
                    return redirect("user_dash/home/")
                else:
                    return render(request,'login.html')
            else:
                messages.error(request,'pleace enter valid email id or password',extra_tags='invalid')
                return redirect("/")      
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
                   return render(request,'reset_password.html',{'type':2})
                else:
                    messages.success(request,"email not exists ")
                    return render(request,'reset_password.html',{'type':1}) 
        elif btn=='2':
                otp=request.POST.get('otp')
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

def add_post(request):
    user=request.user
    users=CoustomUser.objects.get(username=user)
    if users.is_staff:
         return render(request,"staff_pages/add_post.html")
    else:
        return render(request, "user_pages/add_post.html")
    
def message(request): #funtion for msg page render
    user=request.user
    users=CoustomUser.objects.get(username=user)
    if users.is_staff:
         return render(request,"staff_pages/staff_chat.html")
    else:
        return render(request, "user_pages/user_chat.html")
    
from django.shortcuts import render, get_object_or_404  #used for showing profile

def student_detail(request, roll_number):
    user=request.user
    users=CoustomUser.objects.get(username=user)
    student_info=Student.objects.get(id=roll_number)
    post=Post.objects.filter(student__roll_number=student_info.roll_number)  #here student__ will hel to extarct the table field name from the table use double under score
    print(post)
    if users.is_staff:
         return render(request, 'staff_pages/student_detail.html',{'student_info':student_info,'posts':post})
    else:
        return render(request, 'user_pages/student_details.html',{'student_info':student_info,'posts':post})
    

def like_counts(request): #like counts
    posts = Post.objects.all()
    like_counts = {post.id: post.likes.count() for post in posts}
    return JsonResponse(like_counts)

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    student = request.user.student

    # Check if the student has already liked this post
    like, created = Like.objects.get_or_create(post=post, student=student)

    if not created:
        # If the like already exists, delete it (unlike)
        like.delete()
        liked = False
    else:
        # Otherwise, it's a new like
        liked = True

    # Count the total likes for the post
    like_count = post.likes.count()

    return JsonResponse({"liked": liked, "like_count": like_count})

#code for comments

@login_required
def submit_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)
        
        # Save the new comment
        comment = Comment.objects.create(post=post, student=request.user, content=content)
        
        # Return the new comment data as JSON response
        return JsonResponse({
            'success': True,
            'student_name': comment.student.name,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

@login_required
def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by('-created_at').values('student__name', 'content', 'created_at')
    
    return JsonResponse(list(comments), safe=False)