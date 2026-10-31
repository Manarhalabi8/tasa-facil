from django.contrib import admin
from .models import Tasa


@admin.register(Tasa)
class TasaAdmin(admin.ModelAdmin):
    """Administración del modelo Tasa de cambio."""
    list_display = ('fuente', 'fecha', 'valor_bs_por_usd', 'origen')
    list_filter = ('fuente', 'origen', 'fecha')
    search_fields = ('fuente',)
