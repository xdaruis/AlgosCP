from django.urls import path
from . import views

urlpatterns = [
    path('problems/', views.list, name='list'),
    path('problems/<problem_name>/', views.display_problem, name='display_problem'),
    path('send/<problem_id>/', views.send_problem, name='send'),
    path('history/', views.history, name='history'),
]
