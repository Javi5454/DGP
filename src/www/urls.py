from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Dashboard para el administrador
    path('register/', views.register, name='register'),
    path('home_register/', views.home_register, name='home_register'),
    #path('tasks/', include('tasks.urls')),  # Incluye las rutas de la aplicación tasks
]
