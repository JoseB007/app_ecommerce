from django.db import models

from apps.productos.models import Producto
from apps.usuarios.models import Usuario

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
    usuario = models.ForeignKey(Usuario, related_name='ordenes', on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    estado = models.CharField(max_length=20, choices=ESTADO_DE_ORDEN, default=PENDIENTE)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    

class DetalleOrden(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    orden = models.ForeignKey(Orden, related_name="detalle", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='detalles', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden #{self.orden.pk})"
    

class Carrito(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    usuario = models.ForeignKey(Usuario, related_name='carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='carritos', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Carrito de {self.usuario.username})"