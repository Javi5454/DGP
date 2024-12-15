from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from logic.models import Person
from .forms import DynamicTaskForm
from .models import Task
from datetime import date
from django.http import HttpResponseForbidden
from functools import wraps
import os

# Create your views here.
def is_admin(user):
    return user.is_staff

#Decorador para verificar que solo se puede ver la tarea si eres el usuario asignado a ella
def student_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)

        if request.user.person != task.student:
            return HttpResponseForbidden("No tienes permiso para ver esta tarea.")
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

@user_passes_test(is_admin)
def assign_task_1(request):
    persons_with_task_types = Person.objects.filter(task_types__isnull=False).distinct()
    return render(request, 'assign_task_1.html', {'persons': persons_with_task_types})

@user_passes_test(is_admin)
def assign_task2(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(Person, user=user)

    tasks_types = person.task_types.all()

    if request.method == 'POST':
        #Procesar el formulario enviado
        form = DynamicTaskForm(request.POST, request.FILES, tasks_types=tasks_types)

        if form.is_valid():
            task_data = {}

            for field_name, value in form.cleaned_data.items():
                if field_name != 'deadline' and field_name != 'task_name' and field_name != 'requires_completion_file':
                    if field_name == 'Pictograma':
                        subdirectory = 'media/tasks/pictograms'

                        # Crea la subcarpeta si no existe
                        os.makedirs(subdirectory, exist_ok=True)

                        fs = FileSystemStorage(location=subdirectory, base_url=subdirectory)
                        filename = fs.save(value.name, value)
                        file_url = fs.url(filename)
                        task_data[field_name] = '/' + file_url #Conseguir rutas absolutas
                    elif field_name == 'Audio':
                        subdirectory = 'media/tasks/audio'

                        # Crea la subcarpeta si no existe
                        os.makedirs(subdirectory, exist_ok=True)

                        fs = FileSystemStorage(location=subdirectory, base_url=subdirectory)
                        filename = fs.save(value.name, value)
                        file_url = fs.url(filename)
                        task_data[field_name] = '/' + file_url #Conseguir rutas absolutas
                    elif field_name == 'Vídeo':
                        subdirectory = 'media/tasks/video'

                        # Crea la subcarpeta si no existe
                        os.makedirs(subdirectory, exist_ok=True)

                        fs = FileSystemStorage(location=subdirectory, base_url=subdirectory)
                        filename = fs.save(value.name, value)
                        file_url = fs.url(filename)
                        task_data[field_name] = '/' + file_url #Conseguir rutas absolutas
                    else:
                        task_data[field_name] = value

            Task.objects.create(
                    student = person,
                    teacher = request.user.person,
                    task_name = form.cleaned_data['task_name'],
                    assigned_date = date.today(),
                    deadline=form.cleaned_data['deadline'],
                    file_needed=form.cleaned_data['requires_completion_file'],
                    task_data=task_data,
            )
            
            messages.success(request, "La tarea ha sido asignada exitosamente.")
            return redirect(reverse('admin_dashboard'))
        else:
            return render(request, 'assign_task_2.html', {'form': form, 'person': person})

    form = DynamicTaskForm(tasks_types=tasks_types)
    
    return render(request, 'assign_task_2.html', {'form': form, 'person': person})

#View para completar una tarea
@student_only
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        if 'complete' in request.POST:
            #Marcamos la tarea como completada
            task.is_completed = True
            task.save()
            messages.success(request, "Tarea completada exitosamente.")
            return redirect(reverse('dashboard'))
        
        if 'upload_file' in request.FILES:
            #Procesamos el archivo subido
            uploaded_file = request.FILES['upload_file']

            #Guardamos el archivo
            task.completion_file = uploaded_file
            task.save()
            messages.success(request, "Archivo subido exitosamente.")
            return redirect(reverse('dashboard'))
        
    return render(request, 'view_task.html', {'task': task})
