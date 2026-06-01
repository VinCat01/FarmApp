from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import Role, CustomUser


class Command(BaseCommand):
    help = "Создание ролей (Работник, Менеджер, Администратор) и тестовых пользователей"

    def handle(self, *args, **options):
        # === РОЛИ ===
        roles_data = [
            {
                "name": "Работник",
                "codename": "worker",
                "description": "Исполнительный персонал. Выполняет ежедневные задачи: кормление, уборка, сбор продукции и уход за животными.",
            },
            {
                "name": "Менеджер",
                "codename": "manager",
                "description": "Управляющий состав (агрономы, зоотехники). Планирует работы, контролирует процессы и анализирует показатели, управляет закупками.",
            },
            {
                "name": "Администратор",
                "codename": "admin",
                "description": "Полный доступ к управлению системой. Отвечает за настройку системы, управление пользователями, права доступа и администрирование БД.",
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

        # === ПОЛЬЗОВАТЕЛИ ===
        users_data = [
            {
                "username": "admin",
                "password": "VindovCat",
                "full_name": "Главный Администратор",
                "phone": "+7-999-000-00-01",
                "position": "Администратор системы",
                "role_codename": "admin",
                "is_superuser": True,
                "is_staff": True,
            },
            {
                "username": "Vindov.cat",
                "password": "VinCat123",
                "full_name": "Иван Петров",
                "phone": "+7-939-142-22-33",
                "position": "Разнорабочий",
                "role_codename": "worker",
                "is_superuser": False,
                "is_staff": True,
            },
            {
                "username": "anna_manager",
                "password": "ManagerAS",
                "full_name": "Анна Смирнова",
                "phone": "+7-999-444-55-66",
                "position": "Агроном",
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

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка при создании {username}: {e}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Готово! Все роли и пользователи созданы."))
        self.stdout.write("")
        self.stdout.write("Учётные данные для входа:")
        self.stdout.write("  Администратор: admin / VindovCat")
        self.stdout.write("  Работник:       Vindov.cat / VinCat123")
        self.stdout.write("  Менеджер:       anna_manager / ManagerAS")