from django.urls import path
from knox import views as knox_views
from . import api

urlpatterns = [
    path('user/', api.main_user),
    path('register/', api.RegisterAPI.as_view(), name='register'),
    path('login/', api.LoginAPI.as_view(), name='login'),
]  