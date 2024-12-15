from django import forms
from datetime import date

class DynamicTaskForm(forms.Form):
    task_name = forms.CharField(max_length=30, label="Nombre de la tarea")

    deadline = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha límite de realización',
        required=True
    )

    # Campo para indicar si se necesita un archivo de completitud
    requires_completion_file = forms.BooleanField(
        label="¿Se requiere archivo de completitud?",
        required=False,
        initial=False
    )
    #Formulario dinámico que genera campos segúns los TaskType asociados
    def __init__(self, *args, **kwargs):
        taskt_types = kwargs.pop('tasks_types', [])
        super(DynamicTaskForm, self).__init__(*args, **kwargs)

        for task_type in taskt_types:
            if task_type.name == 'Texto':
                self.fields['Texto'] = forms.CharField(
                    label='Descripción de texto',
                    widget=forms.Textarea(attrs={'rows': 3}),
                    required=True
                )
            elif task_type.name == 'Vídeo':
                self.fields['Vídeo'] = forms.FileField(
                    label="Subir archivo de vídeo",
                    required=True
                )
            elif task_type.name == 'Pictograma':
                self.fields['Pictograma'] = forms.ImageField(
                    label="Subir pictograma",
                    required=True
                )
            elif task_type.name == 'Audio':
                self.fields['Audio'] = forms.FileField(
                    label="Subir archivo de audio",
                    required=True
                )
    
    #Verificamos que la deadline es posterior
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if deadline <= date.today():
            raise forms.ValidationError("La fecha límite debe de ser posterior a hoy.")
        return deadline