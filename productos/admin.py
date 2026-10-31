from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Administración del modelo Producto."""
    list_display = ('nombre', 'costo_usd', 'usuario', 'activo')
    list_filter = ('activo', 'unidad_medida')
    search_fields = ('nombre', 'usuario__email')
