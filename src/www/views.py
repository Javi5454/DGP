from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#Página de bienvenida
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "www/home.html")

#Logiun clásico
def login_view(request):
    if request.method == "POST":
        #Pillamos los datos del formulario
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        #Comprobamos que todo ha ido bien
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else: #Si algo no ha ido bien
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('dashboard')

    return render(request, 'login.html')

#Para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')

#Dashboard
@login_required #Decorator for compulsed login
def dashboard(request):
    return render(request, 'dashboard.html')