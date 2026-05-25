from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                # Сохраняем роль пользователя в сессии
                if user.role:
                    request.session["user_role"] = user.role.codename
                else:
                    request.session["user_role"] = "no_role"
                return redirect("/")
        else:
            form = LoginForm()

    return render(request, "registration/login.html", {"form": form})