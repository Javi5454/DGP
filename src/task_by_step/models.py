from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import JSONField
# Create your models here.

class Task(models.Model):
    #Relacion con un estudiante
    student = models.ForeignKey(
        'logic.Person', on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='text_tasks_as_student'
    )

    #Relacion con un profesor
    teacher = models.ForeignKey(
        'logic.Person', on_delete=models.CASCADE, limit_choices_to={'role__in': ['teacher', 'admin']}, related_name='text_tasks_as_teacher'
    )

    #Campos adicionales
    task_name = models.CharField(max_length=100)
    assigned_date = models.DateField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    task_data = JSONField(default=dict)

    #Archivo de completitud
    completion_file = models.FileField(upload_to='completion_files/', null=True, blank=True)

    #Para ver si hace falta archivo
    file_needed = models.BooleanField(default=True)

    def clean(self):
        # Validar que el teacher tenga el rol de "teacher"
        if self.teacher.role == 'student':
            raise ValidationError(f"El usuario {self.teacher.user.get_full_name()} no tiene el rol de 'teacher' o 'admin'.")
        
        # Llamar al método clean de la clase base
        super().clean()

    def save(self, *args, **kwargs):
        # Llamar a clean antes de guardar
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_name} - {self.student.user.get_full_name()}"
    