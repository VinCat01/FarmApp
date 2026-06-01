from django.contrib import admin
from farm.models import (
    Species, Animal, Field, Storage, VetPlan,
    WorkLog, Purchase, SaleOrder, ActionLog, VeterinaryLog, CropRotation
)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ["inventory_number", "species", "gender", "status", "birth_date", "responsible_person"]
    list_filter = ["species", "gender", "status"]
    search_fields = ["inventory_number"]


@admin.register(VeterinaryLog)
class VeterinaryLogAdmin(admin.ModelAdmin):
    list_display = ["animal", "data", "description", "cost"]
    list_filter = ["data"]


@admin.register(VetPlan)
class VetPlanAdmin(admin.ModelAdmin):
    list_display = ["title", "procedure_type", "status", "planned_date", "assigned_to", "estimated_cost"]
    list_filter = ["status", "procedure_type", "planned_date"]
    search_fields = ["title"]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ["cadastral_number", "area", "status"]
    list_filter = ["status"]


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ["name", "item_type", "quantity", "unit"]
    list_filter = ["item_type"]


@admin.register(CropRotation)
class CropRotationAdmin(admin.ModelAdmin):
    list_display = ["field", "crop", "planting_date", "harvest_planned"]


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action_type", "target_repr", "created_at"]
    list_filter = ["action_type", "created_at"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["item", "quantity", "price_per_unit", "supplier", "created_at"]
    list_filter = ["supplier", "created_at"]


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ["item", "quantity", "buyer", "status", "created_at"]
    list_filter = ["status", "created_at"]


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "object_id", "timestamp"]
    list_filter = ["action", "timestamp"]
    readonly_fields = ["user", "action", "model_name", "object_id", "object_repr", "description", "ip_address", "timestamp"]