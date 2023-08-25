import os
import subprocess
import re
import ast
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.contrib import messages
from .models import Problem, Submission
from .forms import SubmissionForm
from decorators.custom_decorators import custom_login_required

RETURN_CODE_TIMEOUT = 124
HUNDRED = 100

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
        if form.is_valid():
            submission = form.save(commit = False)
            submission.user = request.user
            submission.problem = Problem.objects.get(pk = problem_id)

            #Evaluator
            code = form.cleaned_data['code']
            base_path = os.path.join(settings.BASE_DIR, 'Evaluator')
            results = test_submission(problem_id, code, base_path)
            submission.test_cases = results[:-1]
            submission.result = results[-1]
            remove_generated_files(base_path, problem_id)

            submission.save()
            return redirect('submission', submission_id = submission.id)
    messages.success(request, ('Your submission is empty!'))
    problem_name = Problem.objects.get(pk = problem_id).name
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

def test_submission(problem_id, code, base_path):
    problem = Problem.objects.get(pk=problem_id)
    try:
        cpp_path = f"{base_path}/{problem_id}.cpp"
        with open(cpp_path, 'wb') as cpp_file:
            cpp_file.write(code.encode('utf-8'))
        compile_program = f"g++ {cpp_path} -o {base_path}/{problem_id}"
        subprocess.run(compile_program, shell=True, check=True)
        results = []
        test_cases = problem.input.strip().split('#')
        correct_answers = problem.correct_output.strip().split('#')
        test_num = 0
        right_answers = 0
        time_limit_exceeded = False
        for input in test_cases:
            test_num += 1
            try:
                custom_time_limit = problem.time_limit
                execute_program = f"timeout {custom_time_limit} {base_path}/{problem_id} <<< '{input}' > {base_path}/{problem_id}.out"
                subprocess.run(execute_program, shell=True, check=True)
                program_output_file = f"{base_path}/{problem_id}.out"
                with open(program_output_file, 'r') as output_file:
                    program_output = output_file.read().strip()
                if program_output == correct_answers[test_num - 1]:
                    right_answers += 1
                    results.append(f"{test_num}.Correct Solution!")
                else:
                    results.append(f"{test_num}.Wrong Answer")
            except subprocess.CalledProcessError as e:
                if e.returncode == RETURN_CODE_TIMEOUT:
                    time_limit_exceeded = True
                    results.append(f"{test_num}.Time Limit Exceeded")
                else:
                    results.append("Failed Compilation")
        percentage = round(right_answers / test_num) * HUNDRED
        if percentage == HUNDRED:
            results.append("Correct Solution!")
        elif time_limit_exceeded:
            results.append("Time Limit Exceeded!")
        else:
            results.append("Wrong Answers!")
        return results
    except subprocess.CalledProcessError as e:
        return "Failed Compilation"

def remove_generated_files(base_path, problem_id):
    cpp_path = f"{base_path}/{problem_id}.cpp"
    exe_path = f"{base_path}/{problem_id}"
    out_path = f"{base_path}/{problem_id}.out"
    if os.path.exists(cpp_path):
        os.remove(cpp_path)
    if os.path.exists(exe_path):
        os.remove(exe_path)
    if os.path.exists(out_path):
        os.remove(out_path)
