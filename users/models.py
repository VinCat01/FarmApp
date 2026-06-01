from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """Модель роли пользователя"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название роли")
    description = models.TextField(blank=True, verbose_name="Описание")
    codename = models.CharField(max_length=50, unique=True, verbose_name="Кодовое имя")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ("name",)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("worker", "Работник"),
        ("manager", "Менеджер"),
        ("admin", "Администратор"),
    ]

    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    phone = models.CharField(max_length=16, unique=True, verbose_name="Телефон")
    position = models.CharField(max_length=100, verbose_name="Должность")
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Роль",
        related_name="users",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name or self.username

    @property
    def role_display(self):
        return self.get_role_display() if not self.role else self.role.name

    def has_role(self, codename):
        return self.role and self.role.codename == codename

    def is_worker(self):
        return self.has_role("worker")

    def is_manager(self):
        return self.has_role("manager")

    def is_admin_role(self):
        return self.has_role("admin") or self.is_superuser