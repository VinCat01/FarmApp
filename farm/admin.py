from django.contrib import admin
from .models import Employee, Animal

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('tag_number','animal_type','responsible_person','birth_date')
    list_filter = ('animal_type', 'responsible_person', 'birth_date')

