from django.conf import settings
from django.db import models
from django.utils import timezone


class Species(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название вида")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид животного"
        verbose_name_plural = "Виды животных"


class Animal(models.Model):
    GENDER_CHOICES = [("M", "Самец"), ("F", "Самка")]
    STATUS_CHOICES = [
        ("healthy", "Здоров"),
        ("quarantine", "Карантин"),
        ("sick", "Болен"),
    ]
    inventory_number = models.CharField(
        max_length=50, unique=True, verbose_name="Инвентарный номер"
    )
    species = models.ForeignKey(
        Species, on_delete=models.PROTECT, verbose_name="Вид"
    )
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, verbose_name="Пол"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    responsible_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ответственный",
    )

    def __str__(self):
        return f"{self.inventory_number} ({self.species.name})"

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"


class VeterinaryLog(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="vet_records",
        verbose_name="Животное",
    )
    data = models.DateField(auto_now_add=True, verbose_name="Дата")
    description = models.TextField(verbose_name="Описание процедуры/диагноза")
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость", default=0
    )

    def __str__(self):
        return f"{self.animal} - {self.data}"

    class Meta:
        verbose_name = "Вет. запись"
        verbose_name_plural = "Ветеринарный журнал"


class VetPlan(models.Model):
    PROCEDURE_TYPES = [
        ("vaccination", "Вакцинация"),
        ("examination", "Плановый осмотр"),
        ("treatment", "Лечение"),
        ("testing", "Анализ/Диагностика"),
        ("deworming", "Дегельминтизация"),
        ("castration", "Кастрация"),
        ("other", "Другое"),
    ]

    STATUS_CHOICES = [
        ("planned", "Запланирован"),
        ("in_progress", "В процессе"),
        ("completed", "Выполнен"),
        ("cancelled", "Отменён"),
    ]

    title = models.CharField(
        max_length=255, verbose_name="Название процедуры"
    )
    procedure_type = models.CharField(
        max_length=20, choices=PROCEDURE_TYPES, verbose_name="Тип процедуры"
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Вид (группа животных)",
        help_text="Оставьте пустым, если для всех видов",
    )
    planned_date = models.DateField(verbose_name="Плановая дата")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ответственный",
        related_name="vet_plans",
    )
    description = models.TextField(
        blank=True, verbose_name="Описание / Инструкция"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="planned",
        verbose_name="Статус"
    )
    estimated_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name="Предполагаемая стоимость"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кем создан",
        related_name="created_vet_plans",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Вет. план процедуры"
        verbose_name_plural = "Ветеринарные планы работ"
        ordering = ["planned_date", "title"]

    def __str__(self):
        return f"{self.get_procedure_type_display()}: {self.title} ({self.planned_date})"


class Field(models.Model):
    STATUS_CHOICES = [("free", "Свободно"), ("occupied", "Занято")]
    cadastral_number = models.CharField(
        max_length=100, unique=True, verbose_name="Кадастровый номер"
    )
    area = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Площадь (га)"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="free",
        verbose_name="Статус",
    )

    def __str__(self):
        return f"Поле {self.cadastral_number} ({self.area} га)"

    class Meta:
        verbose_name = "Поле"
        verbose_name_plural = "Сельхозполя"


class Storage(models.Model):
    ITEM_TYPE_CHOICES = [
        ("seed", "Семена"),
        ("fertilizer", "Удобрения"),
        ("pesticide", "Пестициды"),
        ("feed", "Корма / Подкормка"),
        ("medicine", "Вет. препараты"),
        ("product_crop", "Растениеводческая продукция"),
        ("product_animal", "Продукция животноводства"),
        ("fuel", "Топливо"),
        ("spare_part", "Запчасти и инструменты"),
        ("inventory", "Инвентарь"),
    ]
    name = models.CharField(max_length=100, verbose_name="Наименование")
    item_type = models.CharField(
        max_length=20, choices=ITEM_TYPE_CHOICES, verbose_name="Тип товара"
    )
    quantity = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Количество"
    )
    unit = models.CharField(
        max_length=10,
        default="шт",
        verbose_name="Единица измерения",
        help_text="кг, л, шт, доз",
    )

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()}) - {self.quantity} {self.unit}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Склад / Запасы"


class CropRotation(models.Model):
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name="crops",
        verbose_name="Поле",
    )
    crop = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT,
        limit_choices_to={"item_type": "seed"},
        verbose_name="Культура",
    )
    planting_date = models.DateField(verbose_name="Дата посадки")
    harvest_planned = models.DateField(verbose_name="Плановый сбор")

    def __str__(self):
        return f"{self.crop.name} на {self.field.cadastral_number}"

    class Meta:
        verbose_name = "Запись севооборота"
        verbose_name_plural = "Севооборот"


class WorkLog(models.Model):
    ACTION_TYPES = [
        ("feeding", "Кормление"),
        ("cleaning", "Уборка/Чистка"),
        ("milking", "Доение"),
        ("weighing", "Взвешивание"),
        ("watering", "Полив"),
        ("harvesting", "Сбор урожая"),
        ("planting", "Посадка"),
        ("treatment", "Обработка"),
        ("moving", "Перемещение"),
        ("other", "Другое"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="work_logs",
    )
    action_type = models.CharField(
        max_length=20, choices=ACTION_TYPES, verbose_name="Тип действия"
    )
    target_type = models.CharField(
        max_length=50, blank=True, verbose_name="Тип объекта"
    )
    target_id = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="ID объекта"
    )
    target_repr = models.CharField(
        max_length=255, blank=True, verbose_name="Объект"
    )
    description = models.TextField(blank=True, verbose_name="Примечание")
    quantity = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name="Объём (кг/л/шт)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время"
    )

    class Meta:
        verbose_name = "Запись в журнале работ"
        verbose_name_plural = "Журнал работ"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.created_at.strftime('%d.%m.%Y %H:%M')} - "
            f"{self.user.full_name or self.user.username}: "
            f"{self.get_action_type_display()} - {self.target_repr}"
        )


class Purchase(models.Model):
    SUPPLIER_CHOICES = [
        ("agro_plus", "АгроПлюс"),
        ("fermer_trade", "ФермерТрейд"),
        ("vet_pharm", "ВетФарм"),
        ("seed_house", "Семенной Дом"),
        ("local", "Местный поставщик"),
        ("other", "Другой"),
    ]

    item = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT,
        verbose_name="Товар",
        related_name="purchases",
    )
    quantity = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Количество"
    )
    price_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за единицу"
    )
    supplier = models.CharField(
        max_length=30, choices=SUPPLIER_CHOICES, verbose_name="Поставщик"
    )
    invoice_number = models.CharField(
        max_length=100, blank=True, verbose_name="Номер накладной"
    )
    purchased_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто приобрёл",
    )
    notes = models.TextField(blank=True, verbose_name="Примечания")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата закупки"
    )

    class Meta:
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки товаров"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item.name} x{self.quantity} ({self.get_supplier_display()})"

    def total_cost(self):
        return self.quantity * self.price_per_unit


class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("approved", "Одобрен"),
        ("completed", "Завершён"),
        ("cancelled", "Отменён"),
    ]

    item = models.ForeignKey(
        Storage,
        on_delete=models.PROTECT,
        verbose_name="Продукция",
        related_name="sales",
        limit_choices_to={"item_type__in": ["product_crop", "product_animal"]},
    )
    quantity = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Количество"
    )
    price_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за единицу (руб)"
    )
    buyer = models.CharField(
        max_length=255, verbose_name="Покупатель"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending",
        verbose_name="Статус"
    )
    notes = models.TextField(blank=True, verbose_name="Примечания")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто создал",
        related_name="sale_orders",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата продажи"
    )

    class Meta:
        verbose_name = "Заказ на продажу"
        verbose_name_plural = "Продажи продукции"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item.name} x{self.quantity} - {self.buyer} ({self.get_status_display()})"

    def total_amount(self):
        return self.quantity * self.price_per_unit


class ActionLog(models.Model):
    ACTION_CATEGORIES = [
        ("create", "Создание"),
        ("update", "Изменение"),
        ("delete", "Удаление"),
        ("view", "Просмотр"),
        ("login", "Вход"),
        ("logout", "Выход"),
        ("other", "Другое"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        related_name="actions",
    )
    action = models.CharField(
        max_length=20, choices=ACTION_CATEGORIES, verbose_name="Действие"
    )
    model_name = models.CharField(
        max_length=100, blank=True, verbose_name="Модель"
    )
    object_id = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="ID объекта"
    )
    object_repr = models.CharField(
        max_length=255, blank=True, verbose_name="Представление объекта"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    ip_address = models.GenericIPAddressField(
        blank=True, null=True, verbose_name="IP-адрес"
    )
    timestamp = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name="Время"
    )
    details = models.JSONField(
        blank=True, null=True, verbose_name="Детали (JSON)"
    )

    class Meta:
        verbose_name = "Запись действия"
        verbose_name_plural = "Журнал действий"
        ordering = ["-timestamp"]

    def __str__(self):
        user_str = (
            self.user.full_name
            if self.user and self.user.full_name
            else (self.user.username if self.user else "Система")
        )
        return (
            f"{self.timestamp.strftime('%d.%m.%Y %H:%M')} - "
            f"{user_str}: {self.get_action_display()} "
            f"{self.model_name} #{self.object_id if self.object_id else ''}"
        )

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        super().save(*args, **kwargs)