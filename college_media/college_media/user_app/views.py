from django.shortcuts import render

# Create your views here.
def welcome(request):
    return render(request,"home.html")

def home(request):
    return render(request,"user_pages/user_home.html")
def add_post(request):
    return render(request,"user_pages/add_post.html")