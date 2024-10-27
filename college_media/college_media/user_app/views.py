from django.shortcuts import render
from user_app.models import *
from staff_app.models import *
from django.shortcuts import get_object_or_404
# Create your views here.
def welcome(request):
    return render(request,"home.html")

def home(request):
    posts=Student.objects.all()
    print(posts)
    return render(request,"user_pages/user_home.html",{'posts':posts})

def add_post(request):
    if request.method=='POST':
        title=request.POST['title']
        body=request.POST['body']
        img=request.FILES['img']
        user=request.user
        student_instence=get_object_or_404(Student, user=user)
        posts=Post.objects.create(student=student_instence,content=body,image=img )
        posts.save()
        print(title,body)
        print("hello there")
        return render(request,"index.html")
    
    return render(request,"user_pages/add_post.html")