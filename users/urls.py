from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.register_request, name='register'),
    path('users/<username>/', views.profile, name='profile'),
    path('users/edit-profile', views.edit_profile, name='edit-profile'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)