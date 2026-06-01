from django import forms
from farm.models import (
    WorkLog, CropRotation, VetPlan, Purchase, SaleOrder
)


class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ["action_type", "target_type", "target_id", "target_repr", "description", "quantity"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class HarvestForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ["target_repr", "quantity", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }
        labels = {
            "target_repr": "Что собрано",
            "quantity": "Объём (кг/л/шт)",
            "description": "Примечание",
        }


class VetPlanForm(forms.ModelForm):
    class Meta:
        model = VetPlan
        fields = [
            "title", "procedure_type", "species", "planned_date",
            "assigned_to", "description", "estimated_cost"
        ]
        widgets = {
            "planned_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class CropRotationForm(forms.ModelForm):
    class Meta:
        model = CropRotation
        fields = ["field", "crop", "planting_date", "harvest_planned"]
        widgets = {
            "planting_date": forms.DateInput(attrs={"type": "date"}),
            "harvest_planned": forms.DateInput(attrs={"type": "date"}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["item", "quantity", "price_per_unit", "supplier", "invoice_number", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ["item", "quantity", "price_per_unit", "buyer", "status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
        }