from django import forms
from logic.models import Person

class PersonalDataForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(
        label='Foto de Perfil', 
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'id': 'id_picture'  # Añadimos el ID necesario para que coincida con el script
        })
    )
class PictogramPasswordForm(forms.Form):
    pictogram_sequence = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
        label='Secuencia de Pictogramas'
    )
