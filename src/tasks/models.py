from django.db import models
import os
from django.conf import settings

# Create your models here.
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


class Menu(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pictogramas/', null=True, blank=True)  # Guardará las imágenes en la carpeta /media/pictogramas

    def save(self, *args, **kwargs):
        # Verificar si el archivo ya existe
        existing_image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)

        if os.path.exists(existing_image_path) and not self._state.adding:  # Solo verifica al editar
            self.image.name = f'pictogramas/{self.image.name}'  # Reutiliza el archivo existente
        super().save(*args, **kwargs)

    def __str__(self):
        return "Menú: {}".format(self.description)
    
class TaskType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name   
