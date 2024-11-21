from django.urls import path
from . import views

urlpatterns = [
    # Ruta para el login con pictogramas
    path('login_pictogram/', views.pictogram_login, name='pictogram_login'),

    # Ruta para los pasos del registro con pictogramas
    path('register_pictogram1/', views.register_pictogram1, name='register_pictogram1'),
    path('register_pictogram2/', views.register_pictogram2, name='register_pictogram2'),
]
