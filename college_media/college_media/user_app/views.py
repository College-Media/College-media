from django.shortcuts import render
from user_app.models import *
from staff_app.models import *
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required

def home(request):
    return render(request,"user_pages/user_home.html")
@login_required
def add_post(request):
    if request.method=='POST':
        title=request.POST['title']
        body=request.POST['body']
        img=request.FILES['img']
        user=request.user
        student_instence=get_object_or_404(Student, user=user)
        posts=Post.objects.create(student=student_instence,content=body,image=img )
        print(title,body)
        print("hello there")
        return render(request,"user_pages/add_post.html")
    return render(request,"user_pages/add_post.html")