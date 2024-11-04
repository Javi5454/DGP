from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),  # Ruta para el registro clásico
    path('register_adapted/', views.register_adapted, name='register_adapted'),  # Ruta para el registro adaptado
    path('home_register/', views.home_register, name='home_register'),  # Ruta para elegir tipo de registro
]
