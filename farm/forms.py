from django import forms
from farm.models import (
    WorkLog, CropRotation, VetPlan, Purchase, SaleOrder, Storage, Animal, Field
)


class WorkLogForm(forms.ModelForm):
    location = forms.CharField(
        max_length=255, required=False,
        label="Место / Загон / Участок",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "напр.: <Загон A1>, <Участок на поле 3>, <Коровник>"})
    )
    target_animal = forms.ModelChoiceField(
        queryset=Animal.objects.all(), required=False,
        label="Животное",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    target_field = forms.ModelChoiceField(
        queryset=Field.objects.all(), required=False,
        label="Поле",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    target_storage = forms.ModelChoiceField(
        queryset=Storage.objects.all(), required=False,
        label="Склад/Запас",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = WorkLog
        fields = ["action_type", "target_type", "target_id", "target_repr", "description", "quantity"]
        widgets = {
            "action_type": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class HarvestForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[
            ("product_crop", "Продукция растениеводства"),
            ("product_animal", "Продукция животноводства"),
        ],
        label="Категория",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    storage_item = forms.ModelChoiceField(
        queryset=Storage.objects.all(), required=False,
        label="Складской запас",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = WorkLog
        fields = ["target_repr", "quantity", "description"]
        widgets = {
            "target_repr": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
        labels = {
            "target_repr": "Название урожая",
            "quantity": "Количество (кг/шт/л)",
            "description": "Описание",
        }


class VetPlanForm(forms.ModelForm):
    class Meta:
        model = VetPlan
        fields = [
            "title", "procedure_type", "species", "planned_date",
            "assigned_to", "description", "estimated_cost"
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "procedure_type": forms.Select(attrs={"class": "form-select"}),
            "species": forms.Select(attrs={"class": "form-select"}),
            "planned_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
            "estimated_cost": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class CropRotationForm(forms.ModelForm):
    class Meta:
        model = CropRotation
        fields = ["field", "crop", "planting_date", "harvest_planned"]
        widgets = {
            "field": forms.Select(attrs={"class": "form-select"}),
            "crop": forms.Select(attrs={"class": "form-select"}),
            "planting_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "harvest_planned": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class PurchaseForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Storage.objects.all(), required=False,
        label="Item",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    new_item_name = forms.CharField(
        max_length=100, required=False,
        label="Название нового товара",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    new_item_type = forms.ChoiceField(
        choices=Storage.ITEM_TYPE_CHOICES, required=False,
        label="Тип",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    new_item_unit = forms.CharField(
        max_length=10, required=False,
        label="Единица измерения",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "кг, шт, л..."}),
        help_text="кг, шт, л, г..."
    )

    class Meta:
        model = Purchase
        fields = ["item", "quantity", "price_per_unit", "supplier", "invoice_number", "notes"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "price_per_unit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "invoice_number": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ["item", "quantity", "price_per_unit", "buyer", "status", "notes"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "price_per_unit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "buyer": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

