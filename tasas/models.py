from django.db import models


class Tasa(models.Model):
    """Modelo para almacenar las tasas de cambio de diferentes fuentes."""

    # Opciones válidas para el campo fuente
    BCV = 'BCV'
    EURO = 'Euro'
    BINANCE = 'Binance'

    FUENTE_CHOICES = [
        (BCV, 'BCV'),
        (EURO, 'Euro'),
        (BINANCE, 'Binance'),
    ]

    # Opciones válidas para el campo origen
    AUTO = 'auto'
    MANUAL = 'manual'

    ORIGEN_CHOICES = [
        (AUTO, 'Automática'),
        (MANUAL, 'Manual'),
    ]

    fuente = models.CharField(
        max_length=20,
        choices=FUENTE_CHOICES,
        help_text='Fuente de donde proviene la tasa de cambio',
    )
    valor_bs_por_usd = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        help_text='Valor en bolívares por un dólar estadounidense',
    )
    fecha = models.DateField(
        help_text='Fecha a la que corresponde la tasa',
    )
    origen = models.CharField(
        max_length=10,
        choices=ORIGEN_CHOICES,
        default=AUTO,
        help_text='Indica si la tasa fue ingresada automáticamente o manualmente',
    )
    creada_en = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora en que se creó el registro',
    )

    class Meta:
        # No permitir tasas duplicadas para la misma fuente y fecha
        unique_together = ('fuente', 'fecha')
        # Ordenar primero por fecha descendente y luego por fuente
        ordering = ['-fecha', 'fuente']

    def __str__(self):
        return f"{self.get_fuente_display()} - {self.fecha}: {self.valor_bs_por_usd} Bs/USD"
