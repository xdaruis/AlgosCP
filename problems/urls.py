from django.urls import path
from . import views

urlpatterns = [
    path('problems', views.list, name='list'),
    path('problems/<problem_name>/', views.problem, name='problem'),
]
