from django.db import models
from logic.models import Person

# Create your models here.
class DinnerTask(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="dinner_tasks")
    name = models.CharField(max_length=200)
    assigned_at = models.DateTimeField(auto_now_add=True) #Fecha y hora de asignacion
    deadline = models.DateTimeField() #Fecha límite de la entrega
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return "Tarea de cena: {} - {} {}".format(self.name, self.student.user.first_name, self.student.user.last_name)
    
    class Meta:
        ordering = ['-assigned_at'] #De más reciente a menos