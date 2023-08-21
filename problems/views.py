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
