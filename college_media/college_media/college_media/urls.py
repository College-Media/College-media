from django.contrib import admin
from django.urls import path,include
from college_media import views # type: ignore


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path('forgot-password',views.password_reset,name="forgot password"),
    path('profile',views.profile,name="profile"), #Showing the profile 
    path('login',views.login_page,name="login"),
    path("admin_dash/",include('admin_app.urls')),
    path("staff_dash/",include('staff_app.urls')),
    path("user_dash/",include('user_app.urls'))
]
