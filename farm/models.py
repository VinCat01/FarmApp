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




class Animal(models.Model):
    TYPE_CHOICES = [
        ('cow','Корова'),
        ('pig','Свинья'),
        ('sheep','Овца'),
    ]
    tag_number = models.CharField(max_length=50, unique=True, verbose_name='номер бирки')
    animal_type = models.CharField(max_length=20,choices=TYPE_CHOICES, verbose_name='Вид животного')
    birth_date = models.DateField(verbose_name='Дата рождения')
    responsible_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name='Ответственный')

    def __str__(self):
        return f"{self.get_animal_type_display()} #{self.tag_number}"

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"

