from django.urls import path,include
from staff_app import views

urlpatterns = [
    path('', views.welcome),
    path("add_student/",views.add_student,name="add_student"),
]