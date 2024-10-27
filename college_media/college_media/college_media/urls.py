from django.contrib import admin
from django.urls import path,include
from college_media import views # type: ignore
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('forgot-password',views.password_reset,name="forgot password"),
    path('profile',views.profile,name="profile"), #Showing the profile 
    path('logout',views.logout_user,name="logout"), #logout url
    path('login',views.login_page,name="login"),
    path("admin_dash/",include('admin_app.urls')),
    path("staff_dash/",include('staff_app.urls')),
    path("user_dash/",include('user_app.urls')),
    path('search_student',views.search_student,name="search_student")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

