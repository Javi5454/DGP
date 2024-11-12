from django.db import models
from django.core.exceptions import ValidationError
from logic.models import Person

# Create your models here.
class Pictogram(models.Model):
    image = models.ImageField(upload_to='pictogramas/')
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description
    
class PictogramSequence(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    sequence = models.ManyToManyField(Pictogram, through='PictogramOrder', related_name='sequences')

    def __str__(self):
        return "Secuencia de pictogramas de {}".format(self.person.user.username)
    
class PictogramOrder(models.Model):
    pictogram_sequence = models.ForeignKey(PictogramSequence, on_delete=models.CASCADE)
    pictogram = models.ForeignKey(Pictogram, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = (('pictogram_sequence', 'pictogram', 'order'))

    def __str__(self):
        return "{} - {}".format(self.pictogram_sequence.person.user.username, self.order)
    
    def clean(self):
        # validamos si el orden es 1 o 2 
        if self.order < 1 or self.order > 2:
            raise ValidationError("El orden debe ser 1 o 2 para una secuencia de dos pictogramas")
        
        # Validar que la secuencia no tenga más de dos pictogramas
        if PictogramOrder.objects.filter(pictogram_sequence=self.pictogram_sequence).count() >= 2:
            raise ValidationError("Solo se permiten dos pictogramas en la secuencia.")