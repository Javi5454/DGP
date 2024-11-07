from django.urls import path
from . import views

urlpatterns = [
    path('login_pictogram/', views.pictogram_login, name='pictogram_login')
]