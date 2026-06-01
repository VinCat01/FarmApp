from django.urls import path
from . import views

app_name = "farm"

urlpatterns = [
    path("", views.index, name="index"),
    path("work-logs/", views.work_log_list, name="work_log_list"),
    path("work-logs/create/", views.work_log_create, name="work_log_create"),
    path("harvest/create/", views.harvest_create, name="harvest_create"),
    path("vet-plans/", views.vet_plan_list, name="vet_plan_list"),
    path("vet-plans/create/", views.vet_plan_create, name="vet_plan_create"),
    path("vet-plans/<int:pk>/", views.vet_plan_detail, name="vet_plan_detail"),
    path("crop-rotation/", views.crop_rotation_list, name="crop_rotation_list"),
    path("crop-rotation/create/", views.crop_rotation_create, name="crop_rotation_create"),
    path("purchases/", views.purchase_list, name="purchase_list"),
    path("purchases/create/", views.purchase_create, name="purchase_create"),
    path("sales/", views.sale_order_list, name="sale_order_list"),
    path("sales/create/", views.sale_order_create, name="sale_order_create"),
    path("sales/<int:pk>/edit/", views.sale_order_edit, name="sale_order_edit"),
    path("sales/<int:pk>/status/", views.sale_order_update_status, name="sale_order_update_status"),
    path("profit-report/", views.profit_report, name="profit_report"),
]