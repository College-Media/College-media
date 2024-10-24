from django.shortcuts import render

# Create your views here.
def welcome(request):
    return render(request,"welcome.html")
def add_student(request):
    return render(request,"staff_pages/add_students.html")