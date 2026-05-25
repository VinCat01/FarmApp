from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from users import views

admin.site.site_header = "Панель управления FarmApp"
admin.site.site_title = "FarmApp Администрирование"
admin.site.index_title = "Добро пожаловать в систему управления фермой"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("farm.urls")),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("login/", views.login_view, name="login"),
]