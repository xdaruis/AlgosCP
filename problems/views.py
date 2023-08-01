from django.shortcuts import render
from .models import Problem

# Create your views here.
def list(request):
    problems = Problem.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})

def problem(request, problem_name):
    problem = Problem.objects.get(name = problem_name.replace('-', ' '))
    return render(request, 'problem.html', {'problem': problem})
