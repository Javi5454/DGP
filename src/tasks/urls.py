from django.urls import path

from . import views

urlpatterns = [
    path('create_dinner_task/', views.create_dinner_task, name='create_dinner_task')
]
