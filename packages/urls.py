from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('', include('problems.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)