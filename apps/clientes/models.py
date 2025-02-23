from django.db import models
from django.forms import model_to_dict
from django.db.models import Sum

from apps.usuarios.models import Usuario
from apps.productos.models import Producto

import uuid

# Create your models here.
class Cliente(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=100)
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, related_name='cliente', blank=True, null=True)
    nombre_completo = models.CharField(max_length=100, blank=True, null=True)
    identificacion = models.CharField(max_length=10, verbose_name='Doc. Identificación', blank=True, null=True)
    telefono = models.CharField(max_length=10, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, verbose_name='Dirección', blank=True, null=True)
    f_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        ordering = ['nombre_completo']


class Carrito(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    cliente = models.OneToOneField(Cliente, related_name='carrito', on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito', related_name='carritos')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return f"Carrito de {self.cliente.nombre_completo}"
    
    def json_carrito(self):
        carrito = model_to_dict(self)
        carrito['productos'] = [producto.json_producto() for producto in self.productos.all()]
        return carrito
    
    def calcular_total(self):
        self.total = sum([item.cantidad * item.producto.precio for item in self.items.all()])
        self.save()

    

class ItemCarrito(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='items_carrito', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item de Carrito'
        constraints = [
            models.UniqueConstraint(fields=['carrito', 'producto'], name='unique_item')
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Carrito de {self.carrito.cliente.nombre_completo})"
    
    def calcular_subtotal(self):
        return self.cantidad * self.producto.precio
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.carrito.calcular_total()