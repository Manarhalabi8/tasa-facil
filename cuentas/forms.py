from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistroForm(UserCreationForm):
    """Formulario para el registro de nuevos usuarios.

    Utiliza el modelo de usuario personalizado y solicita
    los campos username y email.
    """

    class Meta:
        model = User
        fields = ('username', 'email')
