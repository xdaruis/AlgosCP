from django.shortcuts import render, redirect
from .models import Problem
from django.http import HttpResponse

# Create your views here.
def list(request):
    problems = Problem.objects.all().order_by('pk')
    return render(request, 'problems_list.html', {'problems': problems})

def display_problem(request, problem_name):
    problem = Problem.objects.get(name = problem_name.replace('-', ' '))
    return render(request, 'display_problem.html', {'problem': problem})

def send_problem(request, problem_id):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachement; filename={problem_id}.cpp'
    response.writelines(request.POST['code'])
    return response
