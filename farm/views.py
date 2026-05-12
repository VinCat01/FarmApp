from django.shortcuts import render
from .models import Animal, Field, Storage, VeterinaryLog


def index(request):
    animals_count = Animal.objects.count()
    total_area = sum(field.area for field in Field.objects.all())
    low_stock_count = Storage.objects.filter(quantity__lt=10).count()


    latest_operations = VeterinaryLog.objects.select_related('animal').order_by('-data')[:5]

    context = {
        'animals_count': animals_count,
        'total_area': total_area,
        'low_stock_count': low_stock_count,
        'latest_operations': latest_operations,
    }

    return render(request, 'farm/index.html', context)