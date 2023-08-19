from django.shortcuts import render, redirect
from .models import Problem, Submission
from .forms import SubmissionForm
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def list(request):
    problems = Problem.objects.all().order_by('pk')
    return render(request, 'problems_list.html', {'problems': problems})

def display_problem(request, problem_name):
    problem = Problem.objects.get(name = problem_name.replace('-', ' '))
    return render(request, 'display_problem.html', {'problem': problem})

# def send_problem(request, problem_id):
#     response = HttpResponse(content_type='text/plain')
#     response['Content-Disposition'] = f'attachement; filename={problem_id}.cpp'
#     response.writelines(request.POST['code'])
#     return response

def send_problem(request, problem_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SubmissionForm(request.POST)
            if form.is_valid():
                submission = form.save(commit = False)
                submission.user = request.user
                submission.problem = Problem.objects.get(pk = problem_id)
                submission.save()
                return redirect('index') # RETURN EVALUATOR #
        messages.success(request, ('Your submission is empty!'))
        problem_name = Problem.objects.get(pk = problem_id).name
        return redirect('display_problem', problem_name = problem_name)
    return render(request, 'login_required.html', {})

def history(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(user = request.user).order_by('-date')
        return render(request, 'history.html', {'submissions':submissions})
    return render(request, 'login_required.html', {})