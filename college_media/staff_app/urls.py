from django.urls import path,include
from staff_app import views

urlpatterns = [
    path('', views.welcome)
]