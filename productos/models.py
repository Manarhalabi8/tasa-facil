from django.conf import settings
from django.db import models


class Producto(models.Model):
    """Producto del catálogo personal de un usuario."""

    # Opciones válidas para el campo unidad_medida
    UND = 'UND'
    KG = 'KG'
    LT = 'LT'
    M = 'M'

    UNIDAD_MEDIDA_CHOICES = [
        (UND, 'Unidad'),
        (KG, 'Kilogramo'),
        (LT, 'Litro'),
        (M, 'Metro'),
    ]

    # Usuario propietario del producto
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='productos',
        help_text='Usuario al que pertenece este producto',
    )
    nombre = models.CharField(
        max_length=120,
        help_text='Nombre del producto',
    )
    costo_usd = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='Costo del producto en dólares estadounidenses',
    )
    unidad_medida = models.CharField(
        max_length=10,
        choices=UNIDAD_MEDIDA_CHOICES,
        default=UND,
        help_text='Unidad de medida del producto',
    )
    proveedor = models.CharField(
        max_length=120,
        blank=True,
        help_text='Proveedor del producto (opcional)',
    )
    activo = models.BooleanField(
        default=True,
        help_text='Indica si el producto está activo en el catálogo',
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora en que se creó el registro',
    )

    class Meta:
        # Un mismo usuario no puede tener dos productos con el mismo nombre
        unique_together = ('usuario', 'nombre')
        # Ordenar por nombre de forma ascendente
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.costo_usd} USD"
