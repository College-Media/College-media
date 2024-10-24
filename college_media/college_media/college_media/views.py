from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"login.html")

def password_reset(request):
    return render(request,"forgot-password.html")

def profile(request):
    return render(request,"profile.html")