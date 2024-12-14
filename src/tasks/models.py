from django.db import models
import os
from django.conf import settings


############
# DINNERTASK
class DinnerTask(models.Model):
    student = models.ForeignKey('logic.Person', on_delete=models.CASCADE, related_name="dinner_tasks")
    name = models.CharField(max_length=200)
    assigned_at = models.DateTimeField(auto_now_add=True) #Fecha y hora de asignacion
    deadline = models.DateTimeField() #Fecha límite de la entrega
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return "Tarea de cena: {} - {} {}".format(self.name, self.student.user.first_name, self.student.user.last_name)
    
    class Meta:
        ordering = ['-assigned_at'] #De más reciente a menos

###########
# MENU
class Menu(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pictogramas/', null=True, blank=True)  # Guardará las imágenes en la carpeta /media/pictogramas

    def save(self, *args, **kwargs):
    # Si el menú ya existe (es una edición) y tiene una imagen anterior
        if self.pk:
            try:
                existing_menu = Menu.objects.get(pk=self.pk)
                # Compara la imagen anterior con la nueva
                if existing_menu.image and existing_menu.image != self.image:
                    existing_image_path = existing_menu.image.path
                    if os.path.isfile(existing_image_path):
                        os.remove(existing_image_path)  # Elimina la imagen anterior
            except Menu.DoesNotExist:
                pass  # No existe un menú previo, no se hace nada

        # Llama al método save explícitamente con super() bien definido
        super(Menu, self).save(*args, **kwargs)  # Guarda el nuevo menú

    def delete(self, *args, **kwargs):
        # Elimina la imagen asociada al menú cuando se elimina el registro
        if self.image:
            image_path = self.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return "Menú: {}".format(self.description)
    
##########
# CLASSROOM
class Classroom(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pictogramas/', null=True, blank=True)  # Guardará las imágenes en la carpeta /media/pictogramas

    def save(self, *args, **kwargs):
    # Si el aula ya existe (es una edición) y tiene una imagen anterior
        if self.pk:
            try:
                existing_classroom = Classroom.objects.get(pk=self.pk)
                # Compara la imagen anterior con la nueva
                if existing_classroom.image and existing_classroom.image != self.image:
                    existing_image_path = existing_classroom.image.path
                    if os.path.isfile(existing_image_path):
                        os.remove(existing_image_path)  # Elimina la imagen anterior
            except Classroom.DoesNotExist:
                pass  # No existe un menú previo, no se hace nada

        # Llama al método save explícitamente con super() bien definido
        super(Classroom, self).save(*args, **kwargs)  # Guarda el nuevo aula

    def delete(self, *args, **kwargs):
        # Elimina la imagen asociada al menú cuando se elimina el registro
        if self.image:
            image_path = self.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return "Aula: {}".format(self.description)
    

###########
# TASKTYPE    
class TaskType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name   
