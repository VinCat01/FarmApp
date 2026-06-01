from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if request.user.role and request.user.role.codename in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "У вас недостаточно прав для доступа к этой странице.")
            raise PermissionDenied("Недостаточно прав доступа")
        return _wrapped_view
    return decorator


def worker_required(view_func):
    return role_required("worker")(view_func)


def manager_required(view_func):
    return role_required("manager")(view_func)


def admin_role_required(view_func):
    return role_required("admin")(view_func)


def manager_or_admin_required(view_func):
    return role_required("manager", "admin")(view_func)