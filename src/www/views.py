from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Página de bienvenida
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "www/home.html")

# Vista para seleccionar el tipo de registro
def home_register(request):
    return render(request, "www/home_register.html")

# Vista de inicio de sesión clásico
def login_view(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        # Comprobar autenticación
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Si algo no ha ido bien
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('dashboard')

    return render(request, 'login.html')

# Vista de registro clásico
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        # Verificar que las contraseñas coincidan
        if password != password_confirmation:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('login')

    # Renderizar la plantilla de registro en caso de petición GET
    return render(request, 'register.html')

# Vista de registro adaptado
def register_adapted(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        # Verificar que las contraseñas coincidan
        if password != password_confirmation:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register_adapted')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register_adapted')

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Registro adaptado exitoso. Ahora puedes iniciar sesión.")
        return redirect('login')

    return render(request, 'register_adapted.html')

# Para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')

# Dashboard
@login_required  # Decorador para requerir inicio de sesión
def dashboard(request):
    return render(request, 'dashboard.html')
