from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from users.forms import LoginForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                return redirect("farm:index")
            else:
                form.add_error(None, "Ваша учётная запись деактивирована. Обратитесь к администратору.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")