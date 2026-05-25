from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите логин",
        }),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введите пароль",
        }),
    )

    error_messages = {
        "invalid_login": (
            "Неверное имя пользователя или пароль. "
            "Проверьте правильность ввода."
        ),
        "inactive": "Учётная запись деактивирована. Обратитесь к администратору.",
    }