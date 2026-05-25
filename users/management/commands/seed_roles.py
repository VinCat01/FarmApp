"""Команда для создания базовых ролей и тестовых пользователей."""
from django.core.management.base import BaseCommand
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import Role, CustomUser


class Command(BaseCommand):
    help = "Создаёт базовые роли (Работник, Менеджер, Администратор) и тестовых пользователей"

    def handle(self, *args, **options):
        # --- 1. Создание ролей ---
        roles_data = [
            {
                "name": "Работник",
                "codename": "worker",
                "description": "Линейный персонал. Вносит оперативные данные: факты кормления, замеры веса, объемы сбора продукции и перемещение животных.",
            },
            {
                "name": "Менеджер",
                "codename": "manager",
                "description": "Профильный специалист (зоотехник, агроном или управляющий). Формирует планы, работает с поставщиками и покупателями, анализирует отчетность.",
            },
            {
                "name": "Администратор",
                "codename": "admin",
                "description": "Технический специалист. Отвечает за работоспособность системы, учетные записи сотрудников, изменения в справочниках и целостность БД.",
            },
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                codename=role_data["codename"],
                defaults={
                    "name": role_data["name"],
                    "description": role_data["description"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создана роль: {role.name}"))
            else:
                self.stdout.write(f"Роль уже существует: {role.name}")

        # --- 2. Создание тестовых пользователей ---
        users_data = [
            {
                "username": "admin",
                "password": "Admin_2024_Farm!",
                "full_name": "Главный Администратор",
                "phone": "+7-999-000-00-01",
                "position": "Администратор системы",
                "role_codename": "admin",
                "is_superuser": True,
                "is_staff": True,
            },
            {
                "username": "ivan_worker",
                "password": "Worker_2024_Farm!",
                "full_name": "Иван Петров",
                "phone": "+7-999-111-22-33",
                "position": "Разнорабочий",
                "role_codename": "worker",
                "is_superuser": False,
                "is_staff": True,
            },
            {
                "username": "anna_manager",
                "password": "Manager_2024_Farm!",
                "full_name": "Анна Смирнова",
                "phone": "+7-999-444-55-66",
                "position": "Зоотехник",
                "role_codename": "manager",
                "is_superuser": False,
                "is_staff": True,
            },
        ]

        for user_data in users_data:
            username = user_data["username"]
            role = Role.objects.get(codename=user_data["role_codename"])

            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(f"Пользователь {username} уже существует, пропускаем")
                continue

            try:
                # Проверяем пароль на валидность
                validate_password(user_data["password"])

                # Создаём пользователя
                user = CustomUser.objects.create_user(
                    username=username,
                    password=user_data["password"],
                    full_name=user_data["full_name"],
                    phone=user_data["phone"],
                    position=user_data["position"],
                    role=role,
                )
                user.is_staff = user_data["is_staff"]
                user.is_superuser = user_data["is_superuser"]
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Создан пользователь: {username} "
                        f"(роль: {role.name}, пароль: {user_data['password']})"
                    )
                )

            except ValidationError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Пароль для {username} не прошёл валидацию: "
                        f"{'; '.join(e.messages)}"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка при создании {username}: {e}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Готово! Все роли и пользователи созданы."))
        self.stdout.write("")
        self.stdout.write("Тестовые учётные данные:")
        self.stdout.write("  Администратор: admin / Admin_2024_Farm!")
        self.stdout.write("  Работник:       ivan_worker / Worker_2024_Farm!")
        self.stdout.write("  Менеджер:       anna_manager / Manager_2024_Farm!")