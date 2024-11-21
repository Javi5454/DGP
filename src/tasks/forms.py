from django import forms
from .models import DinnerTask
from logic.models import Person
from django.utils.html import format_html

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