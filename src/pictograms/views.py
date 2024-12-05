from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Person, Pictogram, PictogramSequence, PictogramOrder
from .forms import UserRegistrationForm, PictogramPasswordForm
from django.core.files.storage import default_storage
from django.core.files.base import File

import random
import json

def is_admin(user):
    return user.is_staff


def pictogram_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('person_id')
        selected_sequence = data.get('pictogram_sequence', [])

        # Obtener la persona asociada al usuario seleccionado
        person = get_object_or_404(Person, user__username=username)

        # Obtener la secuencia de pictogramas correcta
        try:
            pictogram_sequence = PictogramSequence.objects.get(person=person)
        except PictogramSequence.DoesNotExist:
            return JsonResponse({"error": "Secuencia de pictogramas no encontrada para esta persona."}, status=400)

        correct_sequence = [str(po.pictogram.id) for po in pictogram_sequence.pictogramorder_set.order_by('order')]

        # Verificar si la secuencia seleccionada es correcta
        if selected_sequence == correct_sequence:
            login(request, person.user)  # Iniciar sesión del usuario
            return JsonResponse({"success": True, "redirect_url": "/dashboard"})  # Redirigir al dashboard
        else:
            return JsonResponse({"success": False, "message": "Secuencia incorrecta."})

    # Obtener todos los usuarios con secuencia de pictogramas asociada
    persons = Person.objects.filter(pictogramsequence__isnull=False)

    # Obtener todos los pictogramas para mostrarlos
    all_pictograms = list(Pictogram.objects.all())
    return render(request, 'pictogram_login.html', {'persons': persons, 'pictograms': all_pictograms})




@user_passes_test(is_admin)
def register_pictogram1(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            profile_picture = form.cleaned_data['profile_picture']

            #Guardamos los datos de la sesion
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name

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
            username = f"{request.session['first_name'].lower()}.{request.session['last_name'].lower()}"
            user = User.objects.create_user(
                username=username,
                first_name=request.session['first_name'],
                last_name=request.session['last_name'],
                password="password123"  # Esta es una contraseña por defecto; puedes cambiarla si lo prefieres
            )

            #Recuperamos la iamgen temporal desde el almacenamiento
            temp_file_path = request.session.get('temp_profile_picture')
            with default_storage.open(temp_file_path,'rb') as temp_file:
                profile_picture = File(temp_file)

                # Crear el perfil de persona
                person = Person.objects.create(
                    user=user,
                    picture=profile_picture,
                )

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