import os
import subprocess
import re
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.contrib import messages
from .models import Problem, Submission
from .forms import SubmissionForm

# Create your views here.
def problems_list(request):
    problems = Problem.objects.all().order_by('pk')
    return render(request, 'problems/problems_list.html', {'problems': problems})

def display_problem(request, problem_name):
    problem = Problem.objects.get(name = problem_name.replace('-', ' '))
    return render(request, 'problems/display_problem.html', {'problem': problem})

def send_solution(request, problem_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SubmissionForm(request.POST)
            if form.is_valid():
                submission = form.save(commit = False)
                submission.user = request.user
                submission.problem = Problem.objects.get(pk = problem_id)

                #Evaluator
                code = form.cleaned_data['code']
                base_path = os.path.join(settings.BASE_DIR, 'Evaluator')
                submission.status = test_submission(problem_id, code, base_path)
                remove_generated_files(base_path, problem_id)

                submission.save()
                return redirect('submission', submission_id = submission.id)
        messages.success(request, ('Your submission is empty!'))
        problem_name = Problem.objects.get(pk = problem_id).name
        return redirect('display_problem', problem_name = slugify(problem_name))
    return render(request, 'login_required.html', {})

def history(request):
    if request.user.is_superuser:
        submissions = Submission.objects.all().order_by('-date')
    elif request.user.is_authenticated:
        submissions = Submission.objects.filter(user = request.user).order_by('-date')
    else:
        return render(request, 'login_required.html', {})
    return render(request, 'submissions/history.html', {'submissions':submissions})

def view_submission(request, submission_id):
    submission = Submission.objects.get(pk = submission_id)
    if request.user == submission.user or request.user.is_superuser:
        return render(request, 'submissions/display_submission.html', {'submission': submission})
    messages.success(request, ("You're not allowed to view others submissions!"))
    return redirect('index')

def test_submission(problem_id, code, base_path):
    try:
        # Need to get inputs and outputs from the database in the future
        # problem = Problem.objects.get(pk=problem_id)
        # inputs = problem.input
        # correct_outputs = problem.correct_output
        cpp_file_path = f"{base_path}/{problem_id}.cpp"
        with open(cpp_file_path, 'wb') as cpp_file:
            cpp_file.write(code.encode('utf-8'))
        add_testcases_loop(problem_id, base_path)
        compile_program = f"g++ {cpp_file_path} -o {base_path}/{problem_id}"
        subprocess.run(compile_program, shell=True, check=True)
        execute_program = f"timeout 5 {base_path}/{problem_id} > {base_path}/{problem_id}.out"
        subprocess.run(execute_program, shell=True, check=True)
        compare_results = f"diff {base_path}/DesiredOutputs/{problem_id}.out {base_path}/{problem_id}.out > {base_path}/errors.txt"
        try:
            subprocess.run(compare_results, shell=True, check=True)
            return "Correct Solution!"
        except subprocess.CalledProcessError as e:
            print("Error during result comparison:", e)
            return "Wrong Answer"
    except subprocess.CalledProcessError as e:
        if e.returncode == 124:
            return "Time Limit Exceeded"
        else:
            return "Failed Compilation"

def add_testcases_loop(problem_id, base_path):
    cpp_file_path = f"{base_path}/{problem_id}.cpp"
    with open(cpp_file_path, 'r', encoding='utf-8') as cpp_file:
        cpp_content = cpp_file.read()
    start_testing = f'freopen("{base_path}/Inputs/{problem_id}.in", "r", stdin); int __tests; cin >> __tests; while(__tests--) {{'
    end_testing = ' cout << " "; }'
    with open(cpp_file_path, 'r') as cpp_file:
        cpp_content = cpp_file.read()
    modified_content = re.sub(r'(int\s+main\s*\(\s*\)\s*{)', rf'\1\n    {start_testing}\n', cpp_content, count=1)
    modified_content = re.sub(r'(\s*return\s+0\s*;)', rf'    {end_testing}\n\1', modified_content)
    with open(cpp_file_path, 'w') as cpp_file:
        cpp_file.write(modified_content)

def remove_generated_files(base_path, problem_id):
    cpp_file_path = f"{base_path}/{problem_id}.cpp"
    exe_path = f"{base_path}/{problem_id}"
    out_path = f"{base_path}/{problem_id}.out"
    if os.path.exists(cpp_file_path):
        os.remove(cpp_file_path)
    if os.path.exists(exe_path):
        os.remove(exe_path)
    if os.path.exists(out_path):
        os.remove(out_path)
