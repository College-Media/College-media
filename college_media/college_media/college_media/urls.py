from django.contrib import admin
from django.urls import path,include
from college_media import views # type: ignore
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('forgot-password',views.reset_password,name="forgot password"),
    path('profile',views.profile,name="profile"), #Showing the profile 
    path('logout',views.logout_user,name="logout"), #logout url
    path('login',views.login_page,name="login"),
    path("admin_dash/",include('admin_app.urls')), 
    path('like/<int:post_id>/', views.like_post, name='like_post'), #like url 
    path('like-counts/', views.like_counts, name='like_counts'), #like url 
    path('post/<int:post_id>/submit_comment/', views.submit_comment, name='submit_comment'),#comments
    path('post/<int:post_id>/get_comments/', views.get_comments, name='get_comments'),#comments
    path("chat",views.message,name="message"),
    path('student_details/<str:roll_number>/', views.student_detail, name='student_detail'),
    path("staff_dash/",include('staff_app.urls')),
    path("user_dash/",include('user_app.urls')),
    path('search_student/',views.search_student,name="search_student"),
    path('add_post/',views.add_post,name="Add post")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

