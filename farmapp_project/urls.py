
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('farm.urls')),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.login_view, name='login'),
]
