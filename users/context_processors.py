def user_role(request):
    """Добавляет информацию о роли пользователя в контекст шаблонов"""
    if not request.user.is_authenticated:
        return {
            "user_role": None,
            "is_worker": False,
            "is_manager": False,
            "is_admin_role": False,
        }

    return {
        "user_role": request.user.role.codename if request.user.role else None,
        "is_worker": request.user.is_worker(),
        "is_manager": request.user.is_manager(),
        "is_admin_role": request.user.is_admin_role(),
    }