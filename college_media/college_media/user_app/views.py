from django.shortcuts import render,redirect
from user_app.models import *
from staff_app.models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Student
from django.contrib import messages # type: ignore
from django.utils.timezone import now
from datetime import timedelta
import random
# Create your views here.
def welcome(request):
    return render(request,"home.html")

def home(request):    
    posts = Post.objects.select_related('student').order_by('?') 
    print(request.user.roll_number)
    liked_by=Student.objects.get(roll_number=request.user.roll_number)    
    liked_post_ids = Like.objects.filter(liked_by=liked_by).values_list('post_id', flat=True)
    likes=Like.objects.all()
    commets=Comment.objects.all()
    context=Student.objects.get(roll_number=request.user)
    print(context)
    return render(request,"user_pages/user_home.html",{'posts':posts,'liked_post_ids': set(liked_post_ids),'likes':likes,'coments':commets,'context':context})

def add_post(request):
    roll_number=request.user
    roll_number=Student.objects.get(user=roll_number) 
    tags=Tag.objects.filter(tag_given_by=roll_number)
    unique_tags = {}
    for tag in tags:
        if tag.tag not in unique_tags:
            unique_tags[tag.tag] = tag

    # Convert unique tags dictionary to a list of Tag objects
    unique_tags_list = list(unique_tags.values())
    print(unique_tags_list)
    if request.method=='POST':
        body=request.POST['body']
        img=request.FILES['img']
        user=request.user
        student_instence=get_object_or_404(Student, user=user)
        posts=Post.objects.create(student=student_instence,content=body,image=img ,is_approved=False)
        posts.save()
        messages.success(request,"post sent for verification")
        return redirect('/user_dash/add_post')    
    return render(request,"user_pages/add_post.html",{'tags':unique_tags_list})

def user_profile(request):
    user=request.user
    student_info=Student.objects.get(user=user) 
    post=Post.objects.filter(student__roll_number=student_info.user)
    comments=Comment.objects.filter(student__roll_number=student_info.user) 
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'username':
            username = request.POST['name']
            student_info.name = username
            student_info.save()
            messages.success(request, "User Name Updated", extra_tags='username')
        elif form_type == 'profile_pic':
            if 'img' in request.FILES:
                image_file = request.FILES['img']
                student_info.profile_image = image_file
                student_info.save()
                messages.success(request, "Profile Picture Updated", extra_tags='profile_pic')
            else:
                messages.error(request, "No image file provided.", extra_tags='profile_pic')
    return render(request,"user_pages/user_profile.html",{'student_info':student_info,'posts':post})
    
def tags(request):
    roll_number=request.user
    roll_number=Student.objects.get(user=roll_number) 
    
    tags=Tag.objects.filter(tag_given_by=roll_number)
    unique_tags = {}
    for tag in tags:
        if tag.tag not in unique_tags:
            unique_tags[tag.tag] = tag

    # Convert unique tags dictionary to a list of Tag objects
    unique_tags_list = list(unique_tags.values())
    print(unique_tags_list)
    return render(request, 'user_pages/user_tags.html', {'tags': unique_tags_list})

def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    
    
    if request.method == 'POST':
        if 'new_tag' in request.POST:
            new_tag_value = request.POST['new_tag']
            Tag.objects.filter(tag=tag.tag).update(tag=new_tag_value)
            messages.success(request, "Tag updated successfully", extra_tags="tag_updated")
        else:
            Tag.objects.filter(tag=tag.tag).delete()
            print("deletd tag will be")
            print(tag.tag)
            messages.success(request,"tag deleted successfully",extra_tags="tag_deleted")
    return redirect('tags')  # Redirect back to the user's tag list
def tag_messages(request):
    roll_number=request.user
    roll_number=Student.objects.get(user=roll_number) 
    
    tags=Tag.objects.filter(tag_given_by=roll_number)
    unique_tags = {}
    for tag in tags:
        if tag.tag not in unique_tags:
            unique_tags[tag.tag] = tag

    # Convert unique tags dictionary to a list of Tag objects
    unique_tags_list = list(unique_tags.values())
    print(unique_tags_list)
    return render(request, 'user_pages/tag-messages.html', {'tags': unique_tags_list})

def tag_messages_load(request,tag):
    roll_number=request.user
    roll_number=Student.objects.get(user=roll_number) 
    main_tag=tag
    print("____________________________________________________")
    
    print("tag is :",tag)
    print("-----------------------------------------------------")
    
    tags=Tag.objects.filter(tag_given_by=roll_number)
    unique_tags = {}
    for tag in tags:
        if tag.tag not in unique_tags:
            unique_tags[tag.tag] = tag

    # Convert unique tags dictionary to a list of Tag objects
    unique_tags_list = list(unique_tags.values())
    print(unique_tags_list)
    
    tag_messeges=TagMessage.objects.filter(tag=tag)
    print("_________________________________________")
    
    print(tag_messeges)
    return render(request, 'user_pages/tag-messages.html', {'tags': unique_tags_list,'tag_messeges':tag_messeges,'tag':main_tag})

def multi_tag_messeges(request):
    roll_number=request.user
    roll_number=Student.objects.get(user=roll_number) 
    
    tags=Tag.objects.filter(tag_given_by=roll_number)
    unique_tags = {}
    for tag in tags:
        if tag.tag not in unique_tags:
            unique_tags[tag.tag] = tag

    # Convert unique tags dictionary to a list of Tag objects
    unique_tags_list = list(unique_tags.values())
    print(unique_tags_list)
    return render(request, 'user_pages/multi_tag_messeges.html', {'tags': unique_tags_list})