from django.urls import path,include
from staff_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome),
    path("add_student/",views.add_student,name="add_student"),
    path("add_students/",views.add_students,name="add_students"),
    path("home/",views.home,name="Student_home"),
    path("option_student_add/",views.option_student_add,name="option_student_add"),
    path("staff_post_request",views.staff_post_request,name="staff_post_request"),
    path('approve_or_reject_post/', views.approve_or_reject_post, name='approve_post_or_reject_post'), # type: ignore
    path("staff_profile",views.staff_profile,name="staff_profile"),
    # path("staff_post",views.staff_post,name="staff_post"),
]
