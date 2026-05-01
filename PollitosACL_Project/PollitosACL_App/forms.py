from django import forms
from .models import Usuario

class LoginForm(forms.Form):
    nombre = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput)

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'password', 'rol']
