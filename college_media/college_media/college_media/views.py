from django.shortcuts import render
from django.core.mail import send_mail # type: ignore
from django.conf import settings

# Create your views here.
def home(request):

    return render(request,"login.html")
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
