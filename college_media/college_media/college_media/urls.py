from django.contrib import admin
from django.urls import path,include
from college_media import views # type: ignore
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin_dash/",include('admin_app.urls')), 
    path("staff_dash/",include('staff_app.urls')),
    path("user_dash/",include('user_app.urls')),
    path("chat_app/",include('chat_app.urls')),
    path('',views.login_page,name="login_page"),
    path('forgot-password',views.reset_password,name="forgot password"),
    path('profile',views.profile,name="profile"), #Showing the profile 
    path('logout',views.logout_user,name="logout"), #logout url
    path('login',views.login_page,name="login"),
    # path('add_comment/', views.add_comment, name='add_comment'),
    # path('fetch_comments/<int:post_id>/', views.fetch_comments, name='fetch_comments'),
    path('like/<int:post_id>/', views.like_post, name='like_post'), #like url 
    path('like-counts/', views.like_counts, name='like_counts'), #like url 
    path('post/<int:post_id>/submit_comment/', views.submit_comment, name='submit_comment'),#comments
    path('post/<int:post_id>/get_comments/', views.get_comments, name='get_comments'),#comments
    path("chat",views.message,name="message"),
    path('student_details/<str:roll_number>/', views.student_detail, name='student_detail'),
    path('delete_profile_pic/', views.delete_profile_pic,name='deletepost'),# delete post 
    path('search_student/',views.search_student,name="search_student"),
    path('delete/<int:post_id>', views.deletepost,name='deletepost'),
    path('add_post/',views.add_post,name="Add post"),
    path('get_liked_posts/',views.get_liked_posts,name="get_liked_posts"),
    path('tag_submit',views.tag_submit,name="tag_submit"),
    path('notification',views.notification,name='notification'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

