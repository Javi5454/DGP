from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Person, Pictogram, PictogramSequence, PictogramOrder
from tasks.models import TaskType
from .forms import UserRegistrationForm, PictogramPasswordForm
from django.core.files.storage import default_storage
from django.core.files.base import File

import random
import json

def is_admin(user):
    '''Check if the user is a teacher or admin'''
    try:
        return user.person.role in ['admin']
    except:
        return False

def verify_pictogram(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        sequence = request.POST.get('sequence', '').split(',')

        # Obtener la persona asociada al usuario seleccionado
        person = get_object_or_404(Person, user_id=user_id)
        
        
        try:
            # Obtener la secuencia correcta de pictogramas
            pictogram_sequence = PictogramSequence.objects.get(person=person)
            correct_sequence = [str(po.pictogram.id) for po in pictogram_sequence.pictogramorder_set.order_by('order')]
        except PictogramSequence.DoesNotExist:
            return JsonResponse({"success": False, "message": "No hay secuencia asociada para este usuario."})

        # Validar si la secuencia seleccionada es correcta
        if sequence == correct_sequence:
            return JsonResponse({"success": True, "redirect_url": "/dashboard/"})
        else:
            return JsonResponse({"success": False, "message": "Secuencia incorrecta"})
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


def login_pictogram1(request):
    persons = Person.objects.filter(pictogramsequence__isnull=False).distinct()  # Eliminar duplicados
    return render(request, 'login_pictogram1.html', {'persons': persons})


def login_pictogram2(request, username):
    user = get_object_or_404(User, username=username)
    person = get_object_or_404(Person, user=user)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selections = data.get('selections', [])

            # Verificamos que se hayan seleccionado dos pictogramas
            if len(selections) != 2:
                return JsonResponse({'error': 'Debe seleccionar exactamente dos pictogramas.'}, status=400)
            
            #Obtenemos la secuencia correcta para esta persona
            pictogram_sequence = PictogramSequence.objects.get(person=person)

            correct_sequence = list(PictogramOrder.objects.filter(pictogram_sequence=pictogram_sequence).order_by('order').values_list('pictogram_id', flat=True))

            selected_ids = [int(selection['id']) for selection in selections]


            if selected_ids == correct_sequence:
                login(request, user)
                # Redirige al administrador a `admin_dashboard`, y a otros usuarios al `dashboard`
                if user.is_staff:
                    return JsonResponse({'success': '/admin_dashboard'})
                else:
                    return JsonResponse({'success': '/dashboard'})
            else:
                return JsonResponse({'error': 'Selección incorrecta'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos.'}, status=400)

    #Obtenemos 8 pictogramas, 6 aleatorios
    pictogram_sequence = PictogramSequence.objects.get(person=person)
    person_pictograms = list(pictogram_sequence.sequence.all())

    all_pictograms = Pictogram.objects.exclude(id__in=[p.id for p in person_pictograms])

    #Seleccionamos 6 aleatorios
    random_pictograms = random.sample(list(all_pictograms), 4)

    #Combinamos los resultados
    combined_pictograms = person_pictograms + random_pictograms

    random.shuffle(combined_pictograms)

    return render(request, 'login_pictogram2.html', {'person': person, 'pictograms': combined_pictograms})




@user_passes_test(is_admin)
def register_pictogram1(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            profile_picture = form.cleaned_data['profile_picture']
            username = form.cleaned_data['username']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']

            #Guardamos los datos de la sesion
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['username'] = username
            request.session['password'] = username
            request.session['role'] = role

            request.session['task_types'] = list(form.cleaned_data['task_types'].values_list('id', flat=True))
            print(request.session['task_types'])
            #Guardamos la imagen temporalmente
            file_name = default_storage.save(f"temp/{profile_picture.name}", profile_picture)
            request.session['temp_profile_picture'] = file_name

            return redirect('register_pictogram2')
    else:
        form = UserRegistrationForm()

    return render(request, 'register_pictogram1.html', {'form' : form})


def register_pictogram2(request):
    if request.method == 'POST':
        form = PictogramPasswordForm(request.POST)

        if form.is_valid():
            pictogram_sequence = form.cleaned_data['pictogram_sequence'].split(',')


            if len(pictogram_sequence) != 2:
                messages.error(request, "Debe seleccionar dos pictogramas en el orden deseado.")
                return redirect('register_pictogram2')

            # Crear el usuario
            username = f"{request.session['username']}"
            user = User.objects.create_user(
                username=username,
                first_name=request.session['first_name'],
                last_name=request.session['last_name'],
                password=request.session['password'],  # Esta es una contraseña por defecto; puedes cambiarla si lo prefieres
            )

            #Recuperamos la iamgen temporal desde el almacenamiento
            temp_file_path = request.session.get('temp_profile_picture')
            
            #Recuperamos los tasktype
            task_types_id = request.session['task_types']
            task_types = TaskType.objects.filter(id__in=task_types_id)

            with default_storage.open(temp_file_path,'rb') as temp_file:
                profile_picture = File(temp_file)

                # Crear el perfil de persona
                person = Person.objects.create(
                    user=user,
                    picture=profile_picture,
                    role=request.session['role'],
                )

                person.task_types.set(task_types),

                #Limpiar la imagen temporal anterior si existe
                if temp_file_path:
                    default_storage.delete(temp_file_path)
                    request.session.pop('temp_profile_picture', None)

            #Eliminamos la imagen temporal despues de usarla
            default_storage.delete(temp_file_path)
            request.session.pop('temp_profile_picture', None)

            # Crear la secuencia de pictogramas asociada a la persona
            pictogram_sequence_obj = PictogramSequence.objects.create(person=person)

            # Guardar cada pictograma en el orden seleccionado
            for order, pictogram_id in enumerate(pictogram_sequence, start=1):
                pictogram = get_object_or_404(Pictogram, id=pictogram_id)
                PictogramOrder.objects.create(
                    pictogram_sequence=pictogram_sequence_obj,
                    pictogram=pictogram,
                    order=order
                )

            # Mostrar mensaje de éxito y redirigir al admin_dashboard
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('admin_dashboard')  # Redirige al admin_dashboard tras registro exitoso
    else:
        form = PictogramPasswordForm()

    # Cargar todos los pictogramas para mostrarlos en el formulario
    pictograms = Pictogram.objects.all()
    return render(request, 'register_pictogram2.html', {'form' : form, 'pictograms': pictograms})