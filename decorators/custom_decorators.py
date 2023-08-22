from django.shortcuts import render

def custom_login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        return render(request, 'login_required.html', {})
    return wrapper