from datetime import date, datetime
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from farm.forms import (
    WorkLogForm, HarvestForm, VetPlanForm,
    CropRotationForm, PurchaseForm, SaleOrderForm
)
from farm.models import (
    Animal, Field, Storage, CropRotation, VetPlan,
    WorkLog, Purchase, SaleOrder, ActionLog
)
from users.decorators import role_required


@login_required
def index(request):
    today = timezone.now().date()
    animals_count = Animal.objects.count()
    total_area = Field.objects.aggregate(total=Sum("area"))["total"] or 0
    low_stock_count = Storage.objects.filter(quantity__lt=10).count()

    month_sales = SaleOrder.objects.filter(
        created_at__month=today.month,
        created_at__year=today.year
    )
    month_purchases = Purchase.objects.filter(
        created_at__month=today.month,
        created_at__year=today.year
    )

    month_income = sum(s.total_amount() for s in month_sales.filter(status="completed"))
    month_expenses = sum(p.total_cost() for p in month_purchases)
    month_profit = month_income - month_expenses

    total_sales = SaleOrder.objects.count()
    total_purchases = Purchase.objects.count()
    latest_sales = SaleOrder.objects.order_by("-created_at")[:5]

    upcoming_vet_plans = VetPlan.objects.filter(
        planned_date__gte=today, status__in=["planned", "in_progress"]
    ).order_by("planned_date")[:5]

    latest_work_logs = WorkLog.objects.select_related("user").order_by("-created_at")[:3]
    latest_actions = ActionLog.objects.select_related("user").order_by("-timestamp")[:8]

    context = {
        "animals_count": animals_count,
        "total_area": total_area,
        "low_stock_count": low_stock_count,
        "total_sales": total_sales,
        "total_purchases": total_purchases,
        "month_income": month_income,
        "month_expenses": month_expenses,
        "month_profit": month_profit,
        "upcoming_vet_plans": upcoming_vet_plans,
        "latest_sales": latest_sales,
        "latest_work_logs": latest_work_logs,
        "latest_actions": latest_actions,
    }

    return render(request, "farm/index.html", context)


@login_required
def work_log_list(request):
    logs = WorkLog.objects.select_related("user").order_by("-created_at")
    days = request.GET.get("days")
    if days:
        try:
            days = int(days)
            from_date = timezone.now() - timezone.timedelta(days=days)
            logs = logs.filter(created_at__gte=from_date)
        except ValueError:
            pass
    return render(request, "farm/work_log_list.html", {"logs": logs})


@login_required
def work_log_create(request):
    if request.method == "POST":
        form = WorkLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect("work_log_list")
    else:
        form = WorkLogForm()
    return render(request, "farm/work_log_form.html", {"form": form, "title": "Новая запись"})


@login_required
def harvest_create(request):
    if request.method == "POST":
        form = HarvestForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.action_type = "harvesting"
            log.save()
            return redirect("work_log_list")
    else:
        form = HarvestForm()
    return render(request, "farm/harvest_form.html", {"form": form, "title": "Сбор урожая"})


@role_required("manager", "admin")
def vet_plan_list(request):
    plans = VetPlan.objects.select_related("species", "assigned_to", "created_by").order_by("planned_date")
    status_filter = request.GET.get("status")
    if status_filter:
        plans = plans.filter(status=status_filter)
    return render(request, "farm/vet_plan_list.html", {"plans": plans})


@role_required("manager", "admin")
def vet_plan_create(request):
    if request.method == "POST":
        form = VetPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            return redirect("vet_plan_list")
    else:
        form = VetPlanForm()
    return render(request, "farm/vet_plan_form.html", {"form": form, "title": "Новый вет. план"})


@role_required("manager", "admin")
def vet_plan_detail(request, pk):
    plan = get_object_or_404(VetPlan, pk=pk)
    return render(request, "farm/vet_plan_detail.html", {"plan": plan})


@role_required("manager", "admin")
def crop_rotation_list(request):
    rotations = CropRotation.objects.select_related("field", "crop").all()
    return render(request, "farm/crop_rotation_list.html", {"rotations": rotations})


@role_required("manager", "admin")
def crop_rotation_create(request):
    if request.method == "POST":
        form = CropRotationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crop_rotation_list")
    else:
        form = CropRotationForm()
    return render(request, "farm/crop_rotation_form.html", {"form": form, "title": "Новый севооборот"})


@role_required("manager", "admin")
def purchase_list(request):
    purchases = Purchase.objects.select_related("item", "purchased_by").order_by("-created_at")
    return render(request, "farm/purchase_list.html", {"purchases": purchases})


@role_required("manager", "admin")
def purchase_create(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.purchased_by = request.user
            purchase.save()
            return redirect("purchase_list")
    else:
        form = PurchaseForm()
    return render(request, "farm/purchase_form.html", {"form": form, "title": "Новая закупка"})


@role_required("manager", "admin")
def sale_order_list(request):
    sales = SaleOrder.objects.select_related("item", "created_by").order_by("-created_at")
    status_filter = request.GET.get("status")
    if status_filter:
        sales = sales.filter(status=status_filter)
    return render(request, "farm/sale_order_list.html", {"sales": sales})


@role_required("manager", "admin")
def sale_order_create(request):
    if request.method == "POST":
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            sale.save()
            return redirect("farm:sale_order_list")
    else:
        form = SaleOrderForm()
    return render(request, "farm/sale_order_form.html", {"form": form, "title": "Новая заявка на продажу"})

@login_required
def sale_order_edit(request, pk):
    sale = get_object_or_404(SaleOrder, pk=pk)
    if request.method == "POST":
        form = SaleOrderForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save()
            messages.success(request, "Заявка обновлена.")
            return redirect("farm:sale_order_list")
    else:
        form = SaleOrderForm(instance=sale)
    return render(request, "farm/sale_order_form.html", {"form": form, "title": "Редактирование заявки на продажу"})


@login_required
def sale_order_update_status(request, pk):
    sale = get_object_or_404(SaleOrder, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(SaleOrder.STATUS_CHOICES):
            sale.status = new_status
            sale.save()
            messages.success(request, f"Статус заявки изменён на {sale.get_status_display()}.")
    return redirect("farm:sale_order_list")


@role_required("manager", "admin")
def profit_report(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    today = date.today()
    if not start_date:
        start_date = date(today.year, 1, 1)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if not end_date:
        end_date = today
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    sales = SaleOrder.objects.filter(
        status="completed",
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
    ).select_related("item")

    purchases = Purchase.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
    ).select_related("item")

    vet_plans = VetPlan.objects.filter(
        status="completed",
        updated_at__date__gte=start_date,
        updated_at__date__lte=end_date,
    )

    total_income = sum(s.total_amount() for s in sales)
    total_purchase_cost = sum(p.total_cost() for p in purchases)
    total_vet_cost = sum(v.estimated_cost for v in vet_plans)
    total_expenses = total_purchase_cost + total_vet_cost
    profit = total_income - total_expenses
    profitability_pct = round((profit / total_expenses * 100), 2) if total_expenses > 0 else 0

    context = {
        "title": "Отчёт о прибыли",
        "start_date": start_date,
        "end_date": end_date,
        "sales": sales,
        "purchases": purchases,
        "vet_plans": vet_plans,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_purchase_cost": total_purchase_cost,
        "total_vet_cost": total_vet_cost,
        "profit": profit,
        "profitability_pct": profitability_pct,
        "sales_count": sales.count(),
    }
    return render(request, "farm/profit_report.html", context)