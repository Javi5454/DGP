from django import forms
from logic.models import Person
from www.forms import UserRegistrationForm

class PictogramPasswordForm(forms.Form):
    pictogram_sequence = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
        label='Secuencia de Pictogramas'
    )
