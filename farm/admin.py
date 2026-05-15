from django.contrib import admin
from farmapp_project.settings import AUTH_USER_MODEL
from .models import Species, Animal, VeterinaryLog, Field, Storage, CropRotation


admin.site.site_header = "Панель управления FarmApp"
admin.site.site_title = "FarmApp Админ"
admin.site.index_title = "Управление сельскохозяйственным предприятием"


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('inventory_number', 'species', 'gender', 'status', 'responsible_person', 'birth_date')
    list_filter = ('species', 'status', 'gender')
    search_fields = ('inventory_number',)
    list_editable = ('status',)

@admin.register(VeterinaryLog)
class VeterinaryLogAdmin(admin.ModelAdmin):
    list_display = ('animal', 'data', 'cost')
    list_filter = ('data',)
    search_fields = ('animal__inventory_number', 'description')

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('cadastral_number', 'area', 'status')
    list_filter = ('status',)
    search_fields = ('cadastral_number',)

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'quantity', 'unit')
    list_filter = ('item_type',)
    search_fields = ('name',)

@admin.register(CropRotation)
class CropRotationAdmin(admin.ModelAdmin):
    list_display = ('field', 'crop', 'planting_date', 'harvest_planned')
    list_filter = ('planting_date', 'crop__item_type')
    date_hierarchy = 'planting_date'