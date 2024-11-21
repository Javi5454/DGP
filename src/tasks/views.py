from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import DinnerTask, Menu
from .forms import DinnerTaskForm, MenuForm
import os
from django.conf import settings

# Create your views here.

def is_admin(user):
    '''Check if the user is a teacher or admin'''
    try:
        return user.person.role in ['admin']
    except:
        return False

# CREAR TAREA COMANDA
@user_passes_test(is_admin)
def create_dinner_task(request):
    if request.method == 'POST':
        form = DinnerTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dinner_task_list')
    else:
        form = DinnerTaskForm()
    return render(request, 'create_dinner_task.html', {'form':form})


@user_passes_test(is_admin)
def manage_menus(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            
            # Si no se sube un archivo nuevo, reutiliza el existente
            if not request.FILES.get('image') and form.cleaned_data.get('image'):
                menu.image = form.cleaned_data['image']

            menu.save()
            return redirect('manage_menus')
    else:
        form = MenuForm()

    menus = Menu.objects.all()
    return render(request, 'manage_menus.html', {'form': form, 'menus': menus})


@user_passes_test(is_admin)
def edit_menu(request, menu_id):
    # Obtén la instancia del menú a editar
    old_menu = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear una nueva instancia con los datos del formulario
            new_menu = form.save(commit=False)
            
            # Elimina la instancia anterior
            old_menu.delete()
            
            # Guarda la nueva instancia en la base de datos
            new_menu.save()

            # Redirige a la página de gestión de menús
            return redirect('manage_menus')
    else:
        # Prellenar el formulario con los datos del menú actual
        form = MenuForm(instance=old_menu)
    
    return render(request, 'edit_menu.html', {'form': form, 'menu': old_menu})

@user_passes_test(is_admin)
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('manage_menus')