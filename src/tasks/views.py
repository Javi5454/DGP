from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import DinnerTask, Menu, Classroom, MenuOrder, ClassroomOrder, ClassroomOrderCollection
from .forms import DinnerTaskForm, MenuForm, ClassroomForm
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from django.contrib import messages

# Create your views here.

def is_admin(user):
    return user.is_staff

def dinner_task_detail(request, task_id):
    # Obtén la tarea por su ID
    task = get_object_or_404(DinnerTask, id=task_id)
    return render(request, 'dinner_task1.html', {'task': task})

#Copia profunda de imagen
def deep_copy_image_field(old, new):
    if old.image and old.image.name:
        #Verifica si hay una imagen
        old_image_content = old.image.read()

        #Creamos un archivo con el mismo contenido
        new_image_name = f"copy_of_{old.image.name.split('/')[-1]}"
        new.image.save(new_image_name, ContentFile(old_image_content))

        #Guardamos la nueva instancia
        new.save()

############
# CREAR TAREA COMANDA
@user_passes_test(is_admin)
def create_dinner_task(request):
    if request.method == 'POST':
        form = DinnerTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea comanda comedor asignada correctamente.')
            return redirect('admin_dashboard')
    else:
        form = DinnerTaskForm()
    return render(request, 'create_dinner_task.html', {'form':form})


###############
# COMANDA
def dinner_task1(request, dinnerTask_id):
    classrooms = Classroom.objects.all()
    request.session['taskID']=dinnerTask_id
    return render(request, 'dinner_task1.html', {'classrooms': classrooms})

def dinner_task2(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    taskID = request.session['taskID']
    tarea = get_object_or_404(DinnerTask, pk=taskID)
    menus = Menu.objects.all()

    if request.method == "POST":
        # Crear ClassroomOrder para el aula
        classroom_order = ClassroomOrder.objects.create(classroom=classroom)

        # Recorrer los datos del formulario
        for key, value in request.POST.items():
            if key.startswith("menu_"):
                menu_id = key.split("_")[1]
                quantity = int(value)
                if quantity > 0:
                    menu = get_object_or_404(Menu, pk=menu_id)
                    menu_order = MenuOrder.objects.create(menu=menu, quantity=quantity)
                    classroom_order.menu_orders.add(menu_order)

        # Crear una colección asociada a la tarea
        collection, created = ClassroomOrderCollection.objects.get_or_create(task=tarea)
        collection.classroom_orders.add(classroom_order)

        # Redirigir a dinner_task1 después de guardar
        return redirect('tasks:dinner_task1', dinnerTask_id=taskID)

    return render(request, 'dinner_task2.html', {
        'classroom': classroom,
        'menus': menus,
        'taskid': taskID
    })

##########
# MENU
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
            return redirect('tasks:manage_menus')
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
            
            if not new_menu.image:
                deep_copy_image_field(old_menu, new_menu)
            else:
                new_menu.save()
            
            # Elimina la instancia anterior
            old_menu.delete()

            # Redirige a la página de gestión de menús
            return redirect('tasks:manage_menus')
    else:
        # Prellenar el formulario con los datos del menú actual
        form = MenuForm(instance=old_menu)
    
    return render(request, 'edit_menu.html', {'form': form, 'menu': old_menu})

@user_passes_test(is_admin)
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('tasks:manage_menus')


###################
# CLASSROOOM
@user_passes_test(is_admin)
def manage_classrooms(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST, request.FILES)
        if form.is_valid():
            classroom = form.save(commit=False)
            
            # Si no se sube un archivo nuevo, reutiliza el existente
            if not request.FILES.get('image') and form.cleaned_data.get('image'):
                classroom.image = form.cleaned_data['image']

            classroom.save()
            return redirect('tasks:manage_classrooms')
    else:
        form = ClassroomForm()

    classrooms = Classroom.objects.all()
    return render(request, 'manage_classrooms.html', {'form': form, 'classrooms': classrooms})


@user_passes_test(is_admin)
def edit_classroom(request, classroom_id):
    # Obtén la instancia del aula a editar
    old_classroom = get_object_or_404(Classroom, id=classroom_id)

    if request.method == 'POST':
        form = ClassroomForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear una nueva instancia con los datos del formulario
            new_classroom = form.save(commit=False)
            
            if not new_classroom.image:
                deep_copy_image_field(old_classroom, new_classroom)
            else:
                new_classroom.save()
            
            # Elimina la instancia anterior
            old_classroom.delete()

            # Redirige a la página de gestión de aulas
            return redirect('tasks:manage_classrooms')
    else:
        # Prellenar el formulario con los datos del aula actual
        form = ClassroomForm(instance=old_classroom)
    
    return render(request, 'edit_classroom.html', {'form': form, 'classroom': old_classroom})

@user_passes_test(is_admin)
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    classroom.delete()
    return redirect('tasks:manage_classrooms')

