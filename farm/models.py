from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    phone = models.CharField(max_length=20,verbose_name='Телефон',blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.position})"

    class Meta:
        verbose_name ="Сотрудник"
        verbose_name_plural = "Сотрудники"



class Species(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название вида")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Вид животного"
        verbose_name_plural = "Виды животных"



class Animal(models.Model):
    GENDER_CHOICES = [('M', 'Самец'),
                      ('F', 'Самка')]
    STATUS_CHOICES = [('healthy', 'Здоров'),
                      ('quarantine', 'Карантин'),
                      ('sick', 'Болен'),
                      ]
    inventory_number = models.CharField(max_length=50, unique= True, verbose_name="Инвентарный номер")
    species = models.ForeignKey(Species, on_delete=models.PROTECT, verbose_name="Вид")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    responsible_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="Ответственный")

    def __str__(self):
        return f"{self.inventory_number} ({self.species.name})"

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"



class VeterinaryLog(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE,related_name="vet_records", verbose_name="Животное")
    data = models.DateField(auto_now_add=True, verbose_name="Дата")
    description = models.TextField(verbose_name="Описание мероприятия/диагноз")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Затраты", default=0)

    def __str__(self):
        return f"{self.animal}"

    class Meta:
        verbose_name = "Вет. запись"
        verbose_name_plural = "Журнал ветеринара"

class Field(models.Model):
    STATUS_CHOICES = [('free', 'Свободно'),
                      ('occupied', 'Занято'),
                      ]
    cadastral_number = models.CharField(max_length=100, unique=True,verbose_name="Кадастровый номер")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Площадь(га)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free', verbose_name="Статус")

    def __str__(self):
        return f"Участок {self.cadastral_number} ({self.area}) га"

    class Meta:
        verbose_name = "Поле"
        verbose_name_plural = "Карта полей"



class Storage(models.Model):
    ITEM_TYPE_CHOICES= [('seed','Семена'),
                       ('fertilizer', 'Удобрения'),
                       ('pesticide', 'Химикаты'),
                       ('feed', 'Корма и добавки'),
                       ('medicine', 'Вет препараты'),
                       ('product_crop', 'Собранный урожай'),
                       ('product_animal', 'Продукция животноводства'),
                       ('fuel', 'ГСМ'),
                       ('spare_part', 'Запчасти и расходники'),
                       ('inventory', 'Хоз инвентарь'),
                       ]
    name = models.CharField(max_length=100, verbose_name="Наименование")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, verbose_name="Тип ресурса")
    quantity = models.DecimalField(max_digits=15,decimal_places=2, verbose_name="Количество")
    unit = models.CharField(max_length=10, default='', verbose_name="Единица измерения", help_text="кг, л , шт, тонн")

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()}) - {self.quantity} {self.unit}"

    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Склад / Ресурсы"



class CropRotation(models.Model):
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name='crops', verbose_name="Поле"
    )

    crop = models.ForeignKey(Storage, on_delete=models.PROTECT, limit_choices_to={'item_type': 'seed'},)
    planting_date = models.DateField(verbose_name="Дата посева")
    harvest_planned = models.DateField(verbose_name="Прогноз сбора")

    def __str__(self):
        return f"{self.crop.name} на {self.field.cadastral_number}"

    class Meta:
        verbose_name = "Посев"
        verbose_name_plural = "Севооборот"

