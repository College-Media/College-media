from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("addmin_dash/",include('admin_app.urls')),
    path("staff_dash/",include('staff_app.urls')),
    path("user_dash/",include('user_app.urls'))
]
