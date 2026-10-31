from django.conf import settings
from django.db import models


class Presupuesto(models.Model):
    """Presupuesto de venta con snapshot de la tasa de cambio usada al vender."""

    # Opciones válidas para la fuente de la tasa de venta
    BCV = 'BCV'
    EURO = 'EURO'
    BINANCE = 'BINANCE'
    MANUAL = 'MANUAL'

    TASA_VENTA_FUENTE_CHOICES = [
        (BCV, 'BCV'),
        (EURO, 'Euro'),
        (BINANCE, 'Binance'),
        (MANUAL, 'Manual'),
    ]

    # Opciones válidas para el modo de cálculo del presupuesto
    PRECIO = 'PRECIO'
    PORCENTAJE = 'PORCENTAJE'

    MODO_CHOICES = [
        (PRECIO, 'Precio (conozco el precio de venta)'),
        (PORCENTAJE, 'Porcentaje (quiero un % de ganancia)'),
    ]

    # Usuario propietario del presupuesto
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='presupuestos',
        help_text='Usuario al que pertenece este presupuesto',
    )
    nombre = models.CharField(
        max_length=120,
        help_text='Nombre del presupuesto',
    )
    # Snapshot histórico de la tasa de venta usada al momento de crear el presupuesto
    tasa_venta_fuente = models.CharField(
        max_length=10,
        choices=TASA_VENTA_FUENTE_CHOICES,
        help_text='Fuente de la tasa de venta usada en el presupuesto',
    )
    tasa_venta_valor = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        help_text='Valor de la tasa de venta (Bs por USD) al momento del presupuesto',
    )
    # Modo de cálculo: se conoce el precio de venta o se desea un % de ganancia
    modo = models.CharField(
        max_length=10,
        choices=MODO_CHOICES,
        default=PORCENTAJE,
        help_text='Modo de cálculo del presupuesto',
    )
    porcentaje_ganancia_objetivo = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Porcentaje de ganancia objetivo (opcional)',
    )
    precio_venta_usd_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Precio de venta total en USD (opcional)',
    )
    # Resultados calculados del presupuesto
    total_costo_bs = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        help_text='Costo total del presupuesto en bolívares',
    )
    total_venta_bs = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        help_text='Venta total del presupuesto en bolívares',
    )
    ganancia_bs = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        help_text='Ganancia neta del presupuesto en bolívares',
    )
    porcentaje_ganancia_real = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text='Porcentaje de ganancia real obtenido',
    )
    venta_a_perdida = models.BooleanField(
        default=False,
        help_text='Indica si el presupuesto resulta en pérdida',
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora en que se creó el presupuesto',
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        help_text='Fecha y hora de la última actualización del presupuesto',
    )

    class Meta:
        # Ordenar por los más recientes primero
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} - {self.usuario.email}"


class ItemPresupuesto(models.Model):
    """Ítem de un presupuesto, puede estar vinculado a un producto del catálogo o ser manual."""

    # Opciones válidas para la fuente de la tasa de compra del ítem
    BCV = 'BCV'
    EURO = 'EURO'
    BINANCE = 'BINANCE'
    MANUAL = 'MANUAL'

    TASA_COMPRA_FUENTE_CHOICES = [
        (BCV, 'BCV'),
        (EURO, 'Euro'),
        (BINANCE, 'Binance'),
        (MANUAL, 'Manual'),
    ]

    # Presupuesto al que pertenece este ítem
    presupuesto = models.ForeignKey(
        'Presupuesto',
        on_delete=models.CASCADE,
        related_name='items',
        help_text='Presupuesto al que pertenece este ítem',
    )
    # Producto opcional del catálogo (nulo si el ítem es manual y no está en el catálogo)
    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items_presupuesto',
        help_text='Producto del catálogo asociado (opcional)',
    )
    nombre_snapshot = models.CharField(
        max_length=120,
        help_text='Nombre del ítem al momento de crear el presupuesto',
    )
    costo_usd_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='Costo unitario en dólares estadounidenses',
    )
    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
        help_text='Cantidad del ítem',
    )
    # Snapshot de la tasa de compra para este ítem (puede diferir entre ítems del mismo presupuesto)
    tasa_compra_fuente = models.CharField(
        max_length=10,
        choices=TASA_COMPRA_FUENTE_CHOICES,
        help_text='Fuente de la tasa de compra usada para este ítem',
    )
    tasa_compra_valor = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        help_text='Valor de la tasa de compra (Bs por USD) para este ítem',
    )

    @property
    def subtotal_usd(self):
        """Subtotal en dólares: costo unitario × cantidad."""
        return self.costo_usd_unitario * self.cantidad

    @property
    def subtotal_bs(self):
        """Subtotal en bolívares: subtotal USD × tasa de compra del ítem."""
        return self.subtotal_usd * self.tasa_compra_valor

    def __str__(self):
        return f"{self.nombre_snapshot} x{self.cantidad}"
