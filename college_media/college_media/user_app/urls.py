from django.urls import path,include
from user_app import views

urlpatterns = [
    path('', views.welcome),
    path('/home',views.home,name="home")
]