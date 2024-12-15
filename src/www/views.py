from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from logic.models import Person
from tasks.models import DinnerTask
from task_by_step.models import Task

# Función para verificar si el usuario es un administrador
def is_admin(user):
    '''Check if the user is a teacher or admin'''
    try:
        return user.person.role in ['admin']
    except:
        return False

# Página de bienvenida accesible para todos, muestra opciones de login
def home(request):
    return render(request, "www/home.html")

# Vista de inicio de sesión clásico con redirección condicional
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirige al administrador a `admin_dashboard`, y a otros usuarios al `dashboard`
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    return render(request, 'login.html')

# Dashboard para usuarios generales (estudiantes y profesores)
@login_required
#def dashboard(request):
    # Filtrar tareas solo si el usuario es un estudiante
#    return render(request, 'dashboard.html')

def dashboard(request):
    # Verifica si el usuario tiene un perfil Person
    if hasattr(request.user, 'person'):
        person = request.user.person

        # Solo procesamos si el rol es 'student'
        if person.role == 'student':
            # Obtén todas las tareas asociadas al estudiante y ordénalas por fecha de creación
            dinner_tasks = DinnerTask.objects.filter(student=person, is_completed=False).order_by('assigned_at')  # Orden ascendente
            tasks = Task.objects.filter(student=person, is_completed=False).order_by('assigned_date')  # Orden ascendente
            return render(request, 'dashboard.html', {'dinner_tasks': dinner_tasks, 'tasks': tasks})
    
    # Si no es estudiante, redirige o muestra un mensaje
    return render(request, 'error.html', {'message': 'No tienes permisos para acceder a esta página.'})


# Dashboard específico para administradores
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Vista para seleccionar el tipo de registro, solo visible para administradores
@user_passes_test(is_admin)
def home_register(request):
    return render(request, "www/home_register.html")

# Vista de registro clásico, solo accesible para administradores
@user_passes_test(is_admin)
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Guardar los datos de usuario parcialmente
            user.set_password(form.cleaned_data['password'])  # Establecer la contraseña encriptada
            user.save()  # Guardar el usuario

            # Verificar el rol seleccionado
            role = form.cleaned_data['role']
            if role == 'admin':
                user.is_staff = True  # Permitir acceso al panel de administración
                user.is_superuser = True  # Convertir en superusuario
                user.save()  # Guardar cambios en el usuario

            # Crear el perfil de persona asociado al usuario
            Person.objects.create(
                user=user,
                role=form.cleaned_data['role'],  # Tomar el rol del formulario
                picture=form.cleaned_data['picture']  # Guardar la foto de perfil subida
            )

            # Mensaje de éxito y redirigir
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('admin_dashboard')  # Redirigir al dashboard de administración
        else:
            messages.error(request, "Hubo un error en el formulario. Por favor, revisa los datos.")
    else:
        form = UserRegistrationForm()  # Renderizar un formulario vacío para GET

    return render(request, 'register.html', {'form': form})
# Para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')
