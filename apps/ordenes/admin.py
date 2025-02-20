from django.contrib import admin
from .models import Orden, DetalleOrden, Carrito, ItemCarrito

# Register your models here.
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'valor_total', 'f_creacion', 'estado')


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad', 'precio')


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'f_creacion', 'f_actualizacion')


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'f_creacion')
