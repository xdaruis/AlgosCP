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
            api_url = settings.EVALUATOR_API_URL
            base_path = os.path.join(settings.BASE_DIR, 'problems-test-cases')
            number_of_testcases = problem.number_of_testcases
            inputs = []
            for i in range(1, number_of_testcases + 1):
                with open(f"{base_path}/{problem_id}/{i}.in", 'r') as input_file:
                    inputs.append(input_file.read())
            data = {
                'code': form.cleaned_data['code'],
                'number_of_testcases': number_of_testcases,
                'time_limit': problem.time_limit,
                'inputs': inputs,
            }
            response = requests.post(api_url, data=data)
            if response.status_code == OK_STATUS_CODE:
                results = response.json().get('results', [])
                if results[0] == 'Failed Compilation!':
                    submission.test_cases = ['Please check your code before submitting it!']
                    submission.result = 'Compilation Error!'
                else:
                    slow_solution = False
                    has_wrong_answer = False
                    correct_outputs = []
                    for i in range(1, number_of_testcases + 1):
                        with open(f"{base_path}/{problem_id}/{i}.out", 'r') as output_file:
                            correct_outputs.append(output_file.read())
                    for act_test, act_result in enumerate(results):
                        if act_result == correct_outputs[act_test]:
                            results[act_test] = f"{act_test + 1}.Correct Answer!"
                        elif act_result == f"{act_test + 1}.Time Limit Exceeded":
                            slow_solution = True
                        else:
                            results[act_test] = f"{act_test + 1}.Wrong Answer"
                            has_wrong_answer = True
                    submission.test_cases = results
                    if slow_solution:
                        submission.result = "Suboptimal Solution"
                    elif has_wrong_answer:
                        submission.result = "Partial Test Coverage!"
                    else:
                        submission.result = "Correct Solution!"

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
