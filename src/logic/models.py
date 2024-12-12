import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from tasks.models import TaskType

# To manage uploads of user photos
def person_picture_upload_path(instance, original_filename):
    _, extension = os.path.splitext(original_filename)
    return 'pictures/{filename}--{uuid}{extension}'.format(
        filename = instance.user.username,
        uuid = uuid.uuid4().hex,
        extension=extension # contains the . separator
    )

# Create your models here.
class Person(models.Model):
    ROLE_CHOICES = [
        ('student', 'Alumno'),
        ('teacher', 'Profesor'),
        ('admin', 'Administrador')
    ]

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE
    )
    picture = models.ImageField(upload_to=person_picture_upload_path)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    task_types = models.ManyToManyField(TaskType, related_name='persons')
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return "{}, {} - {}".format(self.user.last_name, self.user.first_name, self.get_role_display())