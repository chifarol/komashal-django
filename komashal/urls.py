
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dbadmin/', admin.site.urls),
    path('api/', include('backend.urls')),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
