from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name='index'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('profilePage/<int:user_id>', views.profilePage, name='profilePage'),
    path('profileUpdates', views.profileUpdates, name='profileUpdates'),
    path('profile', views.profile_list, name='profile'),
    path('project', views.project_list, name='project'),
    path('addProject', views.newProject, name='addProject'),
    
]

urlpatterns=format_suffix_patterns(urlpatterns)