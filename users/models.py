from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    codename = models.CharField(
        max_length=50, unique=True, verbose_name="Кодовое имя"
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class CustomUser(AbstractUser):
    full_name = models.CharField(
        max_length=150, verbose_name="Полное имя", blank=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", blank=True
    )
    position = models.CharField(
        max_length=150, verbose_name="Должность", blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Роль",
        related_name="users",
    )

    def __str__(self):
        return self.full_name or self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"