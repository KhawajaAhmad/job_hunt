from django.contrib import admin
from .models import User, Job, Application

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Application)
