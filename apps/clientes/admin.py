from django.contrib import admin

from .models import Carrito, ItemCarrito

# Register your models here.
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'f_creacion', 'f_actualizacion')


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'f_creacion')