from django.urls import path
from . import views

#Creamos un objeto
urlpatterns = [
    path("",views.index, name="index"),
    path("questions", views.questions, name="questions")
]