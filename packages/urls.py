from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('', include('problems.urls')),
]
