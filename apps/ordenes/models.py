from django.db import models

from apps.productos.models import Producto
from apps.clientes.models import Cliente

import uuid

# Create your models here.
class Orden(models.Model):
    PENDIENTE = 'Pendiente'
    CANCELADA = 'Cancelada'
    ANULADA = 'Anulada'

    ESTADO_DE_ORDEN = [
        (PENDIENTE, 'Pendiente'),
        (CANCELADA, 'Cancelada'),
        (ANULADA, 'Anulada'),
    ]
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    cliente = models.ForeignKey(Cliente, related_name='ordenes', on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    estado = models.CharField(max_length=20, choices=ESTADO_DE_ORDEN, default=PENDIENTE)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre_completo}"
    

class DetalleOrden(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    orden = models.ForeignKey(Orden, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='detalles', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de Orden"
        verbose_name_plural = "Detalles de Orden"
        constraints = [
            models.UniqueConstraint(fields=['orden', 'producto'], name='unique_detalle')
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden #{self.orden.pk})"
    
