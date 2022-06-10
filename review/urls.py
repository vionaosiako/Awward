from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
]