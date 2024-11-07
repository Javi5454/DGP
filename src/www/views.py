from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

# Función para verificar si el usuario es un administrador
def is_admin(user):
    return user.is_staff

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
def dashboard(request):
    return render(request, 'dashboard.html')

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
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('login')

    return render(request, 'register.html')

# Vista de registro adaptado, solo accesible para administradores
@user_passes_test(is_admin)
def register_adapted(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register_adapted')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register_adapted')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Registro adaptado exitoso. Ahora puedes iniciar sesión.")
        return redirect('login')

    return render(request, 'register_adapted.html')

# Para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')
