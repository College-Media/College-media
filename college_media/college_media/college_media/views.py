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
        roll_number = request.POST.get("roll_number")  # Retrieve the roll 
        student = Student.objects.filter(roll_number__icontains=roll_number)
        if not student:
            message="Student not found"
            if users.is_staff:
                return render(request,"staff_pages/staff_search_page.html",{'student':student,'message':message})
            else:
                return render(request, "search.html", {'student': student})  
        else:              
             if users.is_staff:
                return render(request,"staff_pages/staff_search_page.html",{'student':student})
             else:
                return render(request, "search.html", {'student': student})  
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
            
        if btn=='1':
                mail=request.POST.get('mail')
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
                    messages.success(request,"email not exists ",extra_tags='email')
                    return render(request,'reset_password.html',{'type':1}) 
        elif btn=='2':
                otp=request.POST.get('otp')
                a=request.session['a']
                
                if otp==a:
                  return render(request,'reset_password.html',{'type':3})  
                else:
                    messages.success(request,"please enter the correct otp",extra_tags='send_otp')
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
                    messages.success(request,"enter the password correctly",extra_tags='wrong_password')
                    return render(request,'reset_password.html',{'type':3}) 
    return render(request,'reset_password.html',{'type':1})

def add_post(request):
    user=request.user
    users=CoustomUser.objects.get(username=user)
    if request.method=='POST':
        if users.is_staff:       
            body=request.POST['body']
            img=request.FILES['img']
            user=request.user
            student_instence=get_object_or_404(Student, user=user)
            posts=Post.objects.create(student=student_instence,content=body,image=img ,is_approved=True)
            posts.save()
            return render(request,"staff_pages/add_post.html")
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
        like.delete()  # Unlike
        liked = False
    else:
        like.liked_by = student
        like.save()
        liked = True

    # Count the total likes for the post
    like_count = post.likes.count()

    # Return the response
    return JsonResponse({
        "liked": liked,
        "like_count": like_count,
        "liked_by": list(Like.objects.filter(liked_by=student).values_list('post_id', flat=True))
    })

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

def deletepost(request,post_id):
    posts=Post.objects.get(id=post_id)
    posts.delete()
    user=request.user
    if user.is_staff:
        return redirect('staff_profile')
    else:
        return redirect('user_profile')
    
def get_liked_posts(request):
    student = request.user.student
    liked_post_ids = Like.objects.filter(student=student).values_list('post_id', flat=True)
    return JsonResponse({"liked_post_ids": list(liked_post_ids)})

def delete_profile_pic(request):
    user = request.user
    student = Student.objects.get(user=user)

    # Check if the profile picture exists
    if not student.profile_image or not student.profile_image.name:  # Correct condition
        messages.error(request, 'Profile Picture Not Found',extra_tags='profile_notfound')
    else:
        # Delete the profile picture
        student.profile_image.delete(save=False)  # Deletes the file but doesn't save the model
        student.profile_image = None
        student.save()  # Save changes to the database
        messages.success(request, 'Profile Picture Removed Successfully',extra_tags="profile_removed")

    # Redirect based on user type
    if CoustomUser.objects.get(username=user).is_student:
        return redirect("/user_dash/user_profile")
    else:
        return redirect("/staff_dash/staff_profile")

