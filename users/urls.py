from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.register_request, name='register'),
]
