from django.urls import re_path
from django.shortcuts import render
from . import views

urlpatterns = [
re_path(r'.*', views.index)
]