from django.contrib import admin
from user_app.models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)