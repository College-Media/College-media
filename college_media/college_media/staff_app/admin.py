from django.contrib import admin
from staff_app.models import *
# Register your models here.
admin.site.register(CoustomUser)
admin.site.register(Student)
admin.site.register(Tag)
admin.site.register(Main_Notifications)
admin.site.register(TagMessage)