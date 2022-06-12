from django.contrib import admin

# Register your models here.
from .models import Profile, Project
admin.site.register(Profile),
admin.site.register(Project)