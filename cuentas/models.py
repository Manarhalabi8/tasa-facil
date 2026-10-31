from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modelo de usuario personalizado que utiliza el email como identificador de inicio de sesión."""
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class PerfilNegocio(models.Model):
    """Perfil de negocio asociado a un usuario, con datos comerciales y logo opcional."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nombre_negocio = models.CharField(max_length=120, blank=True)
    rif = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"
