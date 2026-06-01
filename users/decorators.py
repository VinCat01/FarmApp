from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            user_role = getattr(request.user, "role", None)
            if user_role and user_role.codename in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("У вас нет доступа к этой странице.")
        return _wrapped_view
    return decorator