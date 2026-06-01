from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, Role


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "full_name", "role", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("full_name", "phone", "position", "role")}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "codename"]