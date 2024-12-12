from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('create_dinner_task/', views.create_dinner_task, name='create_dinner_task'),
    path('manage_menus/', views.manage_menus, name='manage_menus'),
    path('menus/edit/<int:menu_id>/', views.edit_menu, name='edit_menu'),
    path('menus/delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path('manage_classrooms/', views.manage_classrooms, name='manage_classrooms'),
    path('classrooms/edit/<int:classroom_id>/', views.edit_classroom, name='edit_classroom'),
    path('classrooms/delete/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('dinner_task1/', views.dinner_task1, name='dinner_task1'),
    path('dinner_task2/<int:classroom_id>/', views.dinner_task2, name='dinner_task2'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
