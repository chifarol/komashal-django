from django.urls import path
from knox import views as knox_views
from . import api

urlpatterns = [
    path('register/', api.RegisterAPI.as_view(), name='register'),
    path('login/', api.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    
    path('user', api.main_user),
    path('region', api.region),
]  