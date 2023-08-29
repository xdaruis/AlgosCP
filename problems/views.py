import os
import ast
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.contrib import messages
from .models import Problem, Submission
from .forms import SubmissionForm
from decorators.custom_decorators import custom_login_required

OK_STATUS_CODE = 200

# Create your views here.
def problems_list(request):
    problems = Problem.objects.all().order_by('pk')
    return render(request, 'problems/problems_list.html', {'problems': problems})

def display_problem(request, problem_name):
    problem = Problem.objects.get(name = problem_name.replace('-', ' '))
    return render(request, 'problems/display_problem.html', {'problem': problem})

@custom_login_required
def send_solution(request, problem_id):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        problem = Problem.objects.get(pk = problem_id)
        if form.is_valid():
            submission = form.save(commit = False)
            submission.user = request.user
            submission.problem = problem

            # Calling Evaluator API
            api_url = 'http://localhost:8000/api/test-submission/'
            base_path = os.path.join(settings.BASE_DIR, 'problems-test-cases')
            data = {
                'problem_id': problem_id,
                'code': form.cleaned_data['code'],
                'base_path': base_path,
                'number_of_testcases': problem.number_of_testcases,
                'time_limit': problem.time_limit,
            }
            response = requests.post(api_url, data = data)
            if response.status_code == OK_STATUS_CODE:
                results = response.json().get('results', [])
                submission.test_cases = results[:-1]
                submission.result = results[-1]
                submission.save()
            else:
                pass

            submission.save()
            return redirect('submission', submission_id = submission.id)
    messages.success(request, ('Your submission is empty!'))
    problem_name = problem.name
    return redirect('display_problem', problem_name = slugify(problem_name))

@custom_login_required
def history(request):
    if request.user.is_superuser:
        submissions = Submission.objects.all().order_by('-date')
    else:
        submissions = Submission.objects.filter(user = request.user).order_by('-date')
    return render(request, 'submissions/history.html', {'submissions':submissions})

def view_submission(request, submission_id):
    submission = Submission.objects.get(pk = submission_id)
    result_list = ast.literal_eval(submission.test_cases)
    if request.user == submission.user or request.user.is_superuser:
        return render(request, 'submissions/display_submission.html', {'submission': submission, 'result_list':result_list})
    messages.success(request, ("You're not allowed to view others submissions!"))
    return redirect('index')
