from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {})
        messages.success(request, ('Wrong password or username!'))
    return render(request, 'auth/login.html', {})

def logout_request(request):
    logout(request)
    return render(request, 'auth/login.html', {})

def register_request(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request,user)
            return redirect('index')
    return render(request, 'auth/register.html', {'form': form})

def profile(request, username):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = request.user.id)
        return render(request, 'profile.html', {'profile': profile})
    messages.success(request, ("You Must Be Logged In To View This Page..."))
    return redirect('login')
