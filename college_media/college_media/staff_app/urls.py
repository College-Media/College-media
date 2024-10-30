from django.urls import path,include
from staff_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome),
    path("add_student/",views.add_student,name="add_student"),
    path("home/",views.home,name="Student_home"),
    path("option_student_add/",views.add_student,name="option_student_add"),
    path("staff_post_request",views.staff_post_request,name="staff_post_request"),
    path('approve_or_reject_post/', views.approve_or_reject_post, name='approve_post_or_reject_post'), # type: ignore


]
