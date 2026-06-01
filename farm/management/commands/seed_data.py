from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random

from farm.models import (
    Species, Animal, Field, Storage, CropRotation,
    VeterinaryLog, VetPlan, WorkLog, Purchase, SaleOrder
)
from users.models import CustomUser


class Command(BaseCommand):
    help = "Заполнение базы данных тестовыми данными для FarmApp"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Начинаем наполнение базы данных..."))

        # === ПОЛЬЗОВАТЕЛИ (для ссылок) ===
        admin = CustomUser.objects.filter(is_superuser=True).first()
        manager = CustomUser.objects.filter(role__codename="manager").first()
        worker = CustomUser.objects.filter(role__codename="worker").first()
        default_user = admin or CustomUser.objects.first()
        if not default_user:
            self.stdout.write(self.style.ERROR("Нет пользователей! Сначала выполните seed_roles"))
            return

        # === ВИДЫ ЖИВОТНЫХ ===
        species_data = [
            "Крупный рогатый скот",
            "Свиньи",
            "Овцы",
            "Куры",
            "Утки",
            "Лошади",
        ]
        species_objects = []
        for name in species_data:
            obj, created = Species.objects.get_or_create(name=name)
            species_objects.append(obj)
            if created:
                self.stdout.write(f"  Создан вид: {name}")
        self.stdout.write(f"  Виды животных: {len(species_data)} шт.")

        # === ЖИВОТНЫЕ ===
        if Animal.objects.count() < 5:
            genders = ["M", "F"]
            statuses = ["healthy", "healthy", "healthy", "quarantine", "sick"]
            for i in range(20):
                gender = random.choice(genders)
                inv_num = f"Ж-{random.randint(1000, 9999)}-{i+1:03d}"
                species = random.choice(species_objects)
                days_old = random.randint(30, 365 * 6)
                birth = date.today() - timedelta(days=days_old)
                status = random.choice(statuses)
                responsible = random.choice([u for u in [admin, manager, worker] if u])
                Animal.objects.get_or_create(
                    inventory_number=inv_num,
                    defaults={
                        "species": species,
                        "birth_date": birth,
                        "gender": gender,
                        "status": status,
                        "responsible_person": responsible,
                    },
                )
            self.stdout.write(f"  Создано животных: {Animal.objects.count()}")
        else:
            self.stdout.write(f"  Животные уже есть: {Animal.objects.count()} шт.")

        # === ПОЛЯ ===
        field_data = [
            ("90:01:000001:100", 50.5, "free"),
            ("90:01:000001:101", 120.0, "occupied"),
            ("90:01:000001:102", 85.3, "occupied"),
            ("90:01:000001:103", 200.0, "free"),
            ("90:01:000001:104", 45.8, "occupied"),
            ("90:01:000001:105", 150.2, "free"),
        ]
        for cad, area, status in field_data:
            Field.objects.get_or_create(
                cadastral_number=cad,
                defaults={"area": area, "status": status},
            )
        self.stdout.write(f"  Создано полей: {Field.objects.count()}")

        # === СКЛАД ===
        storage_items = [
            # (название, тип, кол-во, ед.изм.)
            ("Пшеница яровая", "seed", 5000, "кг"),
            ("Кукуруза зерновая", "seed", 3000, "кг"),
            ("Ячмень", "seed", 2000, "кг"),
            ("Аммиачная селитра", "fertilizer", 1000, "кг"),
            ("Калий хлористый", "fertilizer", 800, "кг"),
            ("Пестицид широкого спектра", "pesticide", 200, "л"),
            ("Гербицид избирательный", "pesticide", 150, "л"),
            ("Комбикорм для КРС", "feed", 10000, "кг"),
            ("Комбикорм для свиней", "feed", 8000, "кг"),
            ("Зернофураж для птицы", "feed", 5000, "кг"),
            ("Вакцина комплексная", "medicine", 50, "шт"),
            ("Противоглистное средство", "medicine", 200, "доз"),
            ("Дизельное топливо", "fuel", 5000, "л"),
            ("Бензин АИ-92", "fuel", 2000, "л"),
            ("Молоко сырое", "product_animal", 1200, "л"),
            ("Мясо охлаждённое", "product_animal", 500, "кг"),
            ("Яйцо куриное", "product_animal", 15000, "шт"),
            ("Зерно пшеницы", "product_crop", 25000, "кг"),
            ("Зерно кукурузы", "product_crop", 18000, "кг"),
        ]
        for name, item_type, qty, unit in storage_items:
            Storage.objects.get_or_create(
                name=name,
                defaults={"item_type": item_type, "quantity": qty, "unit": unit},
            )
        self.stdout.write(f"  Создано позиций на складе: {Storage.objects.count()}")

        # === СЕВООБОРОТ ===
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
            self.stdout.write(f"  Создано севооборотов: {CropRotation.objects.count()}")
        else:
            self.stdout.write(f"  Севообороты уже есть: {CropRotation.objects.count()}")

        # === ВЕТЕРИНАРНЫЙ ЖУРНАЛ ===
        if VeterinaryLog.objects.count() < 5:
            descriptions = [
                "Плановый осмотр, выявлены признаки авитаминоза",
                "Вакцинация против сибирской язвы",
                "Обработка от паразитов",
                "Лечение мастита, назначен курс антибиотиков",
                "Диагностика беременности, подтверждена",
                "Травма конечности, наложена повязка",
                "Профилактическая дегельминтизация",
            ]
            animals = Animal.objects.all()
            for _ in range(12):
                animal = random.choice(animals)
                desc = random.choice(descriptions)
                cost = round(random.uniform(500, 5000), 2)
                VeterinaryLog.objects.get_or_create(
                    animal=animal,
                    description=desc,
                    defaults={"cost": cost},
                )
            self.stdout.write(f"  Создано записей в вет. журнале: {VeterinaryLog.objects.count()}")
        else:
            self.stdout.write(f"  Вет. журнал уже заполнен: {VeterinaryLog.objects.count()}")

        # === ВЕТЕРИНАРНЫЕ ПЛАНЫ (новая модель!) ===
        if VetPlan.objects.count() < 3:
            procedures = ["vaccination", "examination", "treatment", "testing", "deworming"]
            statuses = ["planned", "planned", "in_progress", "completed"]
            for i in range(5):
                VetPlan.objects.get_or_create(
                    title=f"Плановая процедура #{i+1}",
                    defaults={
                        "procedure_type": random.choice(procedures),
                        "species": random.choice(species_objects + [None]),
                        "planned_date": date.today() + timedelta(days=random.randint(-5, 30)),
                        "assigned_to": random.choice([u for u in [admin, manager, worker] if u]),
                        "description": f"Описание процедуры #{i+1}",
                        "status": random.choice(statuses),
                        "estimated_cost": round(random.uniform(1000, 15000), 2),
                        "created_by": default_user,
                    },
                )
            self.stdout.write(f"  Создано вет. планов: {VetPlan.objects.count()}")
        else:
            self.stdout.write(f"  Вет. планы уже есть: {VetPlan.objects.count()}")

        # === ЖУРНАЛ РАБОТ ===
        if WorkLog.objects.count() < 5:
            action_types = ["feeding", "milking", "harvesting", "cleaning", "treatment", "other"]
            animals = Animal.objects.all()
            fields = Field.objects.all()
            targets = list(animals) + list(fields)
            for i in range(15):
                target = random.choice(targets) if targets else None
                action = random.choice(action_types)
                WorkLog.objects.get_or_create(
                    user=random.choice([u for u in [admin, manager, worker] if u]),
                    action_type=action,
                    defaults={
                        "target_type": target.__class__.__name__ if target else "",
                        "target_id": target.pk if target else None,
                        "target_repr": str(target) if target else "",
                        "description": f"Рабочая операция #{i+1}",
                        "quantity": round(random.uniform(10, 500), 2) if random.random() > 0.3 else None,
                    },
                )
            self.stdout.write(f"  Создано записей в журнале работ: {WorkLog.objects.count()}")
        else:
            self.stdout.write(f"  Журнал работ уже заполнен: {WorkLog.objects.count()}")

        # === ЗАКУПКИ ===
        if Purchase.objects.count() < 3:
            suppliers = ["agro_plus", "fermer_trade", "vet_pharm", "seed_house", "local"]
            items = Storage.objects.all()
            for i in range(8):
                item = random.choice(items)
                qty = random.randint(10, 200)
                price = round(random.uniform(50, 2000), 2)
                Purchase.objects.get_or_create(
                    item=item,
                    quantity=qty,
                    price_per_unit=price,
                    defaults={
                        "supplier": random.choice(suppliers),
                        "purchased_by": default_user,
                        "notes": f"Тестовая закупка #{i+1}",
                    },
                )
            self.stdout.write(f"  Создано закупок: {Purchase.objects.count()}")
        else:
            self.stdout.write(f"  Закупки уже есть: {Purchase.objects.count()}")

        # === ПРОДАЖИ ===
        if SaleOrder.objects.count() < 3:
            statuses = ["pending", "approved", "completed", "cancelled"]
            products = Storage.objects.filter(item_type__in=["product_crop", "product_animal"])
            buyers = ["ООО АгроТорг", "ИП Смирнов", "КФХ Рассвет", "Птицефабрика №1"]
            for i in range(8):
                product = random.choice(products) if products.exists() else None
                if not product:
                    continue
                qty = random.randint(10, 500)
                price = round(random.uniform(30, 500), 2)
                SaleOrder.objects.get_or_create(
                    item=product,
                    quantity=qty,
                    price_per_unit=price,
                    buyer=random.choice(buyers),
                    defaults={
                        "status": random.choice(statuses),
                        "created_by": default_user,
                    },
                )
            self.stdout.write(f"  Создано продаж: {SaleOrder.objects.count()}")
        else:
            self.stdout.write(f"  Продажи уже есть: {SaleOrder.objects.count()}")

        # === ИТОГИ ===
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS("НАПОЛНЕНИЕ БД ЗАВЕРШЕНО!"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"  Виды животных:       {Species.objects.count()}")
        self.stdout.write(f"  Животные:            {Animal.objects.count()}")
        self.stdout.write(f"  Поля:                {Field.objects.count()}")
        self.stdout.write(f"  Склад (позиции):     {Storage.objects.count()}")
        self.stdout.write(f"  Севообороты:         {CropRotation.objects.count()}")
        self.stdout.write(f"  Вет. журнал:         {VeterinaryLog.objects.count()}")
        self.stdout.write(f"  Вет. планы:          {VetPlan.objects.count()}")
        self.stdout.write(f"  Журнал работ:        {WorkLog.objects.count()}")
        self.stdout.write(f"  Закупки:             {Purchase.objects.count()}")
        self.stdout.write(f"  Продажи:             {SaleOrder.objects.count()}")