from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
# router = routers.DefaultRouter()
# router.register('profile',views.ProfileViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('profilePage/<int:user_id>', views.profilePage, name='profilePage'),
    path('profileUpdates', views.profileUpdates, name='profileUpdates'),
    path('profile', views.profile_list),
    # path('api', include(router.urls))
    
]