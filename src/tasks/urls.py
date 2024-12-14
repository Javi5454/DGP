from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'tasks'

urlpatterns = [
    path('create_dinner_task/', views.create_dinner_task, name='create_dinner_task'),
    path('manage_menus/', views.manage_menus, name='manage_menus'),
    path('menus/edit/<int:menu_id>/', views.edit_menu, name='edit_menu'),
    path('menus/delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path('dinner_task/<int:task_id>/', views.dinner_task_detail, name='dinner_task_detail'), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
