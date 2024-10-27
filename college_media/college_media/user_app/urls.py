from django.urls import path,include
from user_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home/',views.home,name="home"),
    path("add_post",views.add_post,name="add_post"),
    path("user_profile",views.user_profile,name="user_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)