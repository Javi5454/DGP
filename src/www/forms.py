from django import forms
from django.contrib.auth.models import User
from logic.models import Person
from tasks.models import TaskType

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellidos")
    role = forms.ChoiceField(choices=Person.ROLE_CHOICES, label="Tipo de Usuario")
    task_types = forms.ModelMultipleChoiceField(queryset=TaskType.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tipos de Tareas")
    profile_picture = forms.ImageField(label="Foto de Perfil", required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
