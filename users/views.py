from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm
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
            messages.success(request, (f'Hello {username}! Let\'s start coding'))
            return redirect('list')
        messages.success(request, ('Wrong password or username!'))
    return render(request, 'auth/login.html', {})

def logout_request(request):
    logout(request)
    return redirect('login')

def register_request(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')
    return render(request, 'auth/register.html', {'form': form})

def profile(request, username):
    if request.user.is_authenticated:
        profile = None
        try:
            user = User.objects.get(username = username)
            profile = Profile.objects.get(user_id = user)
        except:
            pass
        return render(request, 'profile.html', {'profile': profile})
    return render(request, 'login_required.html', {})

def edit_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        form = EditProfileForm(request.POST or None, request.FILES or None, instance = profile)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('profile', username = request.user)
        return render(request, 'edit_profile.html', {'form': form})
    return render(request, 'login_required.html', {})
