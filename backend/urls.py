from django.urls import path
from knox import views as knox_views
from . import api

urlpatterns = [
    path('register/', api.RegisterAPI.as_view(), name='register'),
    path('login/', api.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

     
    #Get and Update user profile
    path('current_user', api.current_user),
    #Create one time super_admin_user admin user
    path('super_admin_user', api.super_admin_user),
    #Create, Update, specific admin user
    path('admin_user', api.admin_user),
    #Create, Read, Update, Delete specific region
    path('region', api.region),
    # fetch regions w/ limits
    path('regions', api.regions),
]  