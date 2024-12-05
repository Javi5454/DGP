from django import forms
from .models import DinnerTask, Menu
from logic.models import Person
from django.utils.html import format_html
import os
from django.conf import settings

class DinnerTaskForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Person.objects.filter(role='student'),
        label="Alumno",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizamos el texto que se muestra en cada opción para incluir la foto
        self.fields['student'].choices = [
            (person.pk, format_html('{}, {} - {}', 
                                    person.user.last_name, person.user.first_name, person.get_role_display()),)
            for person in self.fields['student'].queryset
        ]

    class Meta:
        model = DinnerTask
        fields = ['student', 'name', 'deadline']
        labels = {
            'name': 'Nombre de la tarea',  # Personaliza la etiqueta de 'name'
            'deadline': 'Fecha límite'    # Personaliza la etiqueta de 'deadline'
        }
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Esto incluye fecha y hora
        }



class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['description', 'image']
        labels = {
            'description': 'Nombre del Menú',
            'image': 'Seleccionar o Cargar Pictograma',
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            import os
            from django.conf import settings

            # Verificar si el archivo ya existe
            image_path = os.path.join(settings.MEDIA_ROOT, 'pictogramas', image.name)
            if os.path.exists(image_path):
                # Reutilizar la imagen existente
                return f'pictogramas/{image.name}'

        return image