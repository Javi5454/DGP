from django.urls import path
from . import views


urlpatterns = [
    # Ruta para el login con pictogramas
    path('login_pictogram1/', views.login_pictogram1, name='login_pictogram1'),
    path('login_pictogram2/<str:username>/', views.login_pictogram2, name='login_pictogram2'),

    # Ruta para los pasos del registro con pictogramas
    path('register_pictogram1/', views.register_pictogram1, name='register_pictogram1'),
    path('register_pictogram2/', views.register_pictogram2, name='register_pictogram2'),

    path('verify_pictogram/', views.verify_pictogram, name='verify_pictogram'),
    #path('dashboard/', views.dashboard, name='dashboard'),
]
