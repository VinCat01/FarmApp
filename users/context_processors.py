def user_role(request):
    if request.user.is_authenticated:
        role = getattr(request.user, "role", None)
        return {
            "user_role": role.codename if role else None,
            "is_worker": role and role.codename == "worker",
            "is_manager": role and role.codename == "manager",
            "is_admin_role": role and role.codename == "admin",
        }
    return {
        "user_role": None,
        "is_worker": False,
        "is_manager": False,
        "is_admin_role": False,
    }