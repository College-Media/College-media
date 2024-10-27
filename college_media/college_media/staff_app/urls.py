from django.urls import path,include
from staff_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.welcome),
    path("add_student/",views.add_student,name="add_student"),
    path("home/",views.home,name="Student_home")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)