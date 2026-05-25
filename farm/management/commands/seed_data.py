"""Кастомная команда для заполнения БД тестовыми данными."""
from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random

from farm.models import Species, Animal, Field, Storage, CropRotation, VeterinaryLog
from users.models import CustomUser


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Начинаем заполнение БД тестовыми данными..."))

        # 1. Создаём тестового пользователя
        if not CustomUser.objects.filter(username="admin").exists():
            user = CustomUser.objects.create_superuser(
                username="admin",
                password="admin123",
                full_name="Иван Петров",
                phone="+7-999-111-22-33",
                position="Главный агроном",
            )
            self.stdout.write(f"  Создан пользователь: {user.username}")
        else:
            user = CustomUser.objects.get(username="admin")
            self.stdout.write(f"  Пользователь уже существует: {user.username}")

        # 2. Виды животных
        species_data = [
            "Крупный рогатый скот",
            "Свиньи",
            "Овцы",
            "Куры",
            "Лошади",
            "Козы",
        ]
        species_objects = []
        for name in species_data:
            obj, created = Species.objects.get_or_create(name=name)
            species_objects.append(obj)
            if created:
                self.stdout.write(f"  Добавлен вид: {name}")
        self.stdout.write(f"  Виды животных: {len(species_data)} шт.")

        # 3. Животные (15 шт.)
        if Animal.objects.count() < 10:
            for i in range(15):
                gender = random.choice(["M", "F"])
                inv_num = f"Ж-{random.randint(1000, 9999)}-{i+1:03d}"
                species = random.choice(species_objects)
                days_old = random.randint(30, 365 * 5)
                birth = date.today() - timedelta(days=days_old)
                status = random.choice(["healthy", "healthy", "healthy", "quarantine", "sick"])
                Animal.objects.get_or_create(
                    inventory_number=inv_num,
                    defaults={
                        "species": species,
                        "birth_date": birth,
                        "gender": gender,
                        "status": status,
                        "responsible_person": user,
                    },
                )
            self.stdout.write(f"  Добавлено животных: {Animal.objects.count()}")
        else:
            self.stdout.write(f"  Животные уже есть: {Animal.objects.count()} шт.")

        # 4. Поля
        field_data = [
            ("90:01:000001:100", 50.5, "free"),
            ("90:01:000001:101", 120.0, "occupied"),
            ("90:01:000001:102", 85.3, "occupied"),
            ("90:01:000001:103", 200.0, "free"),
            ("90:01:000001:104", 45.8, "free"),
            ("90:01:000001:105", 150.2, "occupied"),
        ]
        for cad, area, status in field_data:
            Field.objects.get_or_create(
                cadastral_number=cad,
                defaults={"area": area, "status": status},
            )
        self.stdout.write(f"  Добавлено полей: {Field.objects.count()}")

        # 5. Склад
        storage_items = [
            ("Пшеница озимая", "seed", 5000, "кг"),
            ("Ячмень яровой", "seed", 3000, "кг"),
            ("Кукуруза", "seed", 2000, "кг"),
            ("Аммиачная селитра", "fertilizer", 1000, "кг"),
            ("Нитроаммофоска", "fertilizer", 800, "кг"),
            ("Гербицид Торнадо", "pesticide", 200, "л"),
            ("Инсектицид Фуфанон", "pesticide", 150, "л"),
            ("Комбикорм для КРС", "feed", 10000, "кг"),
            ("Комбикорм для свиней", "feed", 8000, "кг"),
            ("Зерносмесь для кур", "feed", 5000, "кг"),
            ("Тетрациклин", "medicine", 50, "шт"),
            ("Вакцина от сибирской язвы", "medicine", 200, "доз"),
            ("Дизельное топливо", "fuel", 5000, "л"),
            ("Бензин АИ-92", "fuel", 2000, "л"),
            ("Масло моторное", "spare_part", 100, "л"),
        ]
        for name, item_type, qty, unit in storage_items:
            Storage.objects.get_or_create(
                name=name,
                defaults={"item_type": item_type, "quantity": qty, "unit": unit},
            )
        self.stdout.write(f"  Добавлено позиций на склад: {Storage.objects.count()}")

        # 6. Севооборот
        if CropRotation.objects.count() < 3:
            fields_occupied = Field.objects.filter(status="occupied")
            seeds = Storage.objects.filter(item_type="seed")
            for field in fields_occupied:
                if seeds.exists():
                    CropRotation.objects.get_or_create(
                        field=field,
                        crop=random.choice(seeds),
                        defaults={
                            "planting_date": date.today() - timedelta(days=random.randint(30, 120)),
                            "harvest_planned": date.today() + timedelta(days=random.randint(30, 180)),
                        },
                    )
            self.stdout.write(f"  Добавлено записей севооборота: {CropRotation.objects.count()}")
        else:
            self.stdout.write(f"  Севооборот уже есть: {CropRotation.objects.count()}")

        # 7. Ветеринарный журнал
        if VeterinaryLog.objects.count() < 5:
            descriptions = [
                "Плановый осмотр, состояние удовлетворительное",
                "Вакцинация от ящура",
                "Обработка от паразитов",
                "Лечение мастита, назначены антибиотики",
                "Обрезка копыт, обработка",
                "Роды, телёнок здоров",
                "Профилактический осмотр",
            ]
            animals = Animal.objects.all()
            for _ in range(10):
                animal = random.choice(animals)
                desc = random.choice(descriptions)
                cost = round(random.uniform(500, 5000), 2)
                VeterinaryLog.objects.get_or_create(
                    animal=animal,
                    description=desc,
                    defaults={"cost": cost},
                )
            self.stdout.write(f"  Добавлено записей в ветжурнал: {VeterinaryLog.objects.count()}")
        else:
            self.stdout.write(f"  Ветжурнал уже заполнен: {VeterinaryLog.objects.count()}")

        self.stdout.write(self.style.SUCCESS("БД успешно заполнена тестовыми данными!"))