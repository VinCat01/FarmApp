from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from django.db.models import Count, Sum, Avg
from .models import Species, Animal, VeterinaryLog, Field, Storage, CropRotation


admin.site.site_header = "Панель управления FarmApp"
admin.site.site_title = "FarmApp Администрирование"
admin.site.index_title = "Добро пожаловать в систему управления фермой"


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def link_to_model(obj, field_name="__str__"):
    """Создаёт HTML-ссылку на объект в админке"""
    url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.pk])
    return mark_safe(f'<a href="{url}">{getattr(obj, field_name)}</a>')


# === SPECIES ===
@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("name", "animal_count")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(animal_count=Count("animal"))

    @admin.display(description="Количество животных")
    def animal_count(self, obj):
        return obj.animal_count


# === ANIMAL ===
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "inventory_number",
        "species",
        "gender_colored",
        "status",
        "status_colored",
        "birth_date",
        "age_display",
        "responsible_person",
    )
    list_filter = ("species", "status", "gender", "birth_date")
    search_fields = ("inventory_number", "species__name")
    list_editable = ("status",)
    list_per_page = 20
    date_hierarchy = "birth_date"

    fieldsets = (
        ("Основная информация", {
            "fields": ("inventory_number", "species", "gender", "birth_date")
        }),
        ("Статус и ответственность", {
            "fields": ("status", "responsible_person")
        }),
    )

    @admin.display(description="Пол")
    def gender_colored(self, obj):
        if obj.gender == "M":
            return mark_safe('<span style="color: #0d6efd;">♂ Самец</span>')
        return mark_safe('<span style="color: #dc3545;">♀ Самка</span>')

    @admin.display(description="Статус")
    def status_colored(self, obj):
        colors = {"healthy": "green", "quarantine": "orange", "sick": "red"}
        labels = {"healthy": "Здоров", "quarantine": "Карантин", "sick": "Болен"}
        color = colors.get(obj.status, "gray")
        label = labels.get(obj.status, obj.status)
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{label}</span>')

    @admin.display(description="Возраст")
    def age_display(self, obj):
        from datetime import date
        days = (date.today() - obj.birth_date).days
        years = days // 365
        months = (days % 365) // 30
        if years > 0:
            return f"{years}г {months}мес"
        return f"{months}мес"


# === VETERINARY LOG ===
@admin.register(VeterinaryLog)
class VeterinaryLogAdmin(admin.ModelAdmin):
    list_display = ("animal_link", "data", "short_description", "cost_display")
    list_filter = ("data", "animal__species")
    search_fields = ("animal__inventory_number", "description")
    date_hierarchy = "data"

    @admin.display(description="Животное")
    def animal_link(self, obj):
        return link_to_model(obj.animal, "inventory_number")

    @admin.display(description="Описание")
    def short_description(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description

    @admin.display(description="Стоимость")
    def cost_display(self, obj):
        return mark_safe(f'<strong>{obj.cost} ₽</strong>')


# === FIELD ===
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("cadastral_number", "area_display", "status_colored", "crop_count")
    list_filter = ("status",)
    search_fields = ("cadastral_number",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(crop_count=Count("crops"))

    @admin.display(description="Площадь (га)")
    def area_display(self, obj):
        return f"{obj.area} га"

    @admin.display(description="Статус")
    def status_colored(self, obj):
        color = "green" if obj.status == "free" else "blue"
        label = "Свободно" if obj.status == "free" else "Занято"
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{label}</span>')

    @admin.display(description="Культур")
    def crop_count(self, obj):
        return obj.crop_count


# === STORAGE ===
@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ("name", "item_type_colored", "quantity_display", "unit", "low_stock_warning")
    list_filter = ("item_type",)
    search_fields = ("name",)
    list_per_page = 20

    @admin.display(description="Тип")
    def item_type_colored(self, obj):
        colors = {
            "seed": "#198754",
            "fertilizer": "#6f42c1",
            "pesticide": "#dc3545",
            "feed": "#fd7e14",
            "medicine": "#0dcaf0",
            "fuel": "#ffc107",
        }
        color = colors.get(obj.item_type, "#6c757d")
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{obj.get_item_type_display()}</span>')

    @admin.display(description="Количество")
    def quantity_display(self, obj):
        return f"{obj.quantity}"

    @admin.display(description="Статус")
    def low_stock_warning(self, obj):
        if obj.quantity < 100:
            return mark_safe('<span style="color: red;">⚠ Мало</span>')
        return mark_safe('<span style="color: green;">✓ В норме</span>')


# === CROP ROTATION ===
@admin.register(CropRotation)
class CropRotationAdmin(admin.ModelAdmin):
    list_display = ("field_link", "crop_link", "planting_date", "harvest_planned", "days_until_harvest")
    list_filter = ("planting_date", "harvest_planned", "crop__item_type")
    date_hierarchy = "planting_date"

    @admin.display(description="Поле")
    def field_link(self, obj):
        return link_to_model(obj.field, "cadastral_number")

    @admin.display(description="Культура")
    def crop_link(self, obj):
        return link_to_model(obj.crop, "name")

    @admin.display(description="До сбора (дней)")
    def days_until_harvest(self, obj):
        from datetime import date
        delta = (obj.harvest_planned - date.today()).days
        if delta < 0:
            return mark_safe(f'<span style="color: orange;">Просрочено на {-delta} дн.</span>')
        elif delta < 30:
            return mark_safe(f'<span style="color: red; font-weight: bold;">{delta} дн.</span>')
        return f"{delta} дн."