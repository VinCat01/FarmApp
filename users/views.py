from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('/')
        else:
            form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})