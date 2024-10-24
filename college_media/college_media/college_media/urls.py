from django.contrib import admin
from django.urls import path,include
import college_media.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="home"),
    path("addmin_dash/",include('admin_app.urls')),
    path("staff_dash/",include('staff_app.urls')),
    path("user_dash/",include('user_app.urls'))
]
