from django.urls import path
from . import views

app_name = 'task_by_step'

urlpatterns = [
    # Ruta para el login con pictogramas
    path('assign_task1/', views.assign_task_1, name='assign_task1'),
    path('assign_task2/<str:username>/', views.assign_task2, name='assign_task2'),
    path('view_task/<int:task_id>/', views.view_task , name='view_task')
]
