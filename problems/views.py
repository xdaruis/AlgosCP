from django.shortcuts import render, redirect
from .models import Problem
from django.http import HttpResponse

# Create your views here.
def list(request):
    problems = Problem.objects.all()
    return render(request, 'problems_list.html', {'problems': problems})

def display_problem(request, problem_name):
    problem = Problem.objects.get(name = problem_name.replace('-', ' '))
    return render(request, 'display_problem.html', {'problem': problem})

def send_problem(request, problem_name):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachement; filename=solution.cpp'

    # lines = [ace.edit('editor').getSession().getValue()]
    lines = [Problem.objects.get(name = problem_name).template]
    response.writelines(lines)
    return response