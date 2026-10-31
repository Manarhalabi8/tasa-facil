from django.contrib import admin
from .models import Presupuesto, ItemPresupuesto


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    """Administración del modelo Presupuesto."""
    list_display = ('nombre', 'usuario', 'modo', 'total_venta_bs', 'creado_en')
    list_filter = ('modo', 'tasa_venta_fuente')
    search_fields = ('nombre', 'usuario__email')


@admin.register(ItemPresupuesto)
class ItemPresupuestoAdmin(admin.ModelAdmin):
    """Administración del modelo ItemPresupuesto."""
    list_display = ('nombre_snapshot', 'presupuesto', 'cantidad', 'costo_usd_unitario')
