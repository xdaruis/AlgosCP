from django.urls import path
from . import views

urlpatterns = [
    path('problems/', views.problems_list, name='list'),
    path('problems/<problem_name>/', views.display_problem, name='display_problem'),
    path('problems/<problem_id>/send', views.send_solution, name='send'),
    path('submission/<submission_id>/', views.view_submission, name='submission'),
    path('history/', views.history, name='history'),
]
