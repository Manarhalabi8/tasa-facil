from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PerfilNegocio


@admin.register(User)
class UserAdminConfig(UserAdmin):
    """Administración del modelo User personalizado."""
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)


@admin.register(PerfilNegocio)
class PerfilNegocioAdmin(admin.ModelAdmin):
    """Administración del modelo PerfilNegocio."""
    list_display = ('user', 'nombre_negocio', 'rif')
    search_fields = ('user__email', 'nombre_negocio')
