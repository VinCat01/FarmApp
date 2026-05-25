from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "codename", "description", "user_count")
    search_fields = ("name", "codename")

    def get_queryset(self, request):
        from django.db.models import Count
        return super().get_queryset(request).annotate(user_count=Count("users"))

    @admin.display(description="Пользователей")
    def user_count(self, obj):
        return obj.user_count


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "full_name",
        "role_display",
        "position",
        "phone",
        "email",
        "is_staff",
    )
    list_filter = ("role", "is_staff", "is_superuser", "position")
    search_fields = ("username", "full_name", "phone", "email")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {
            "fields": ("full_name", "phone", "position", "role")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительная информация", {
            "fields": ("full_name", "phone", "position", "role")
        }),
    )

    @admin.display(description="Роль")
    def role_display(self, obj):
        if not obj.role:
            return "-"
        colors = {
            "worker": "green",
            "manager": "blue",
            "admin": "red",
        }
        color = colors.get(obj.role.codename, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.role.name,
        )